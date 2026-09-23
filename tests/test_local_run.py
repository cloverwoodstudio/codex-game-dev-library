"""Small real Bash processes; hermetic roots never touch production Mac locks.

The copied script changes only the literal SYSTEM_TMP path. getconf/df/mkdir are
fixture commands. A separately recorded Mac smoke test exercises production roots.
"""
import json
import os
from pathlib import Path
import shlex
import signal
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASH = "/bin/bash"

class LocalRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="cw-lock-test-")
        self.base = Path(self.tmp.name).resolve()
        self.addCleanup(self.tmp.cleanup)
        self.running = []
        self.addCleanup(self.stop_all)
        self.system = self.base / "system"
        self.canonical = self.base / "canonical with space"
        self.a = self.base / "caller-a"
        self.b = self.base / "caller-b"
        self.bin = self.base / "bin"
        for path in (self.system, self.canonical, self.a, self.b, self.bin):
            path.mkdir()
        source = (ROOT / "scripts/cloverwood-local-run.sh").read_text()
        self.assertEqual(source.count("SYSTEM_TMP=/tmp\n"), 1)
        self.script = self.base / "local-run.sh"
        self.script.write_text(source.replace("SYSTEM_TMP=/tmp\n", "SYSTEM_TMP=" + shlex.quote(str(self.system)) + "\n", 1))
        self.tool("getconf", '#!/bin/sh\n[ "${TEST_GETCONF_FAIL:-0}" = 0 ] || exit 1\nprintf "%s\\n" "$TEST_CANONICAL"\n')
        self.tool("df", '#!/bin/sh\nprintf "Filesystem 1024-blocks Used Available Capacity Mounted\\nfixture 90000000 1 %s 1%% /\\n" "${TEST_FREE_KIB:-31457280}"\n')
        self.tool("mkdir", '#!/bin/sh\nfor arg do case "$arg" in */results) [ "${TEST_SETUP_FAIL:-0}" = 0 ] || exit 1 ;; esac; done\nexec /bin/mkdir "$@"\n')

    def tool(self, name, source):
        path = self.bin / name
        path.write_text(source)
        path.chmod(0o700)

    def env(self, tmp=None, run="run", heavy="1", **extra):
        env = os.environ.copy()
        for key in list(env):
            if key.startswith(("CLOVERWOOD_", "TEST_")):
                del env[key]
        env.update(TMPDIR=str(tmp or self.a), CLOVERWOOD_REPO_NAME="test-repo",
                   CLOVERWOOD_RUN_ID=run, CLOVERWOOD_EXCLUSIVE_MAC=heavy,
                   CLOVERWOOD_MIN_FREE_GIB="20", TEST_CANONICAL=str(self.canonical),
                   PATH=str(self.bin) + ":/usr/bin:/bin")
        env.update(extra)
        return env

    def launch(self, command, env=None):
        proc = subprocess.Popen([BASH, str(self.script), "--", *command], cwd=self.base,
                                env=env or self.env(), stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                start_new_session=True)
        self.running.append(proc)
        return proc

    def finish(self, proc, expected=0, data=None):
        out, err = proc.communicate(input=data, timeout=10)
        self.assertEqual(proc.returncode, expected, out + err)
        return out + err

    def stop_all(self):
        for proc in self.running:
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGKILL)
            proc.communicate(timeout=5)

    def lock(self, root):
        return root / "cloverwood-ci/.mac-heavy.lock"

    def run_root(self, root=None, run="run"):
        return (root or self.a) / "cloverwood-ci/test-repo" / run

    def assert_clear(self, *roots):
        for root in roots or (self.system, self.canonical, self.a):
            self.assertFalse(self.lock(root).exists(), str(root))

    def wait_ready(self, ready, proc):
        deadline = time.monotonic() + 5
        while not ready.exists() and time.monotonic() < deadline:
            if proc.poll() is not None:
                self.fail("child exited before readiness: " + str(proc.communicate()))
            time.sleep(0.01)
        self.assertTrue(ready.exists(), "bounded readiness timeout")

    def held(self, env=None, name="holder"):
        ready, release = self.base / (name + "-ready"), self.base / (name + "-release")
        code = ("import os,time; from pathlib import Path; "
                f"Path({str(ready)!r}).write_text(str(os.getppid())); "
                f"deadline=time.monotonic()+8\nwhile not Path({str(release)!r}).exists() and time.monotonic()<deadline: time.sleep(.01)")
        self.addCleanup(release.touch)
        proc = self.launch([sys.executable, "-B", "-c", code], env)
        self.wait_ready(ready, proc)
        return proc, release

    def test_success_exports_and_exact_argument_stdin_forwarding(self):
        code = 'import os,sys,json; print(json.dumps({"stdin":sys.stdin.read(),"args":sys.argv[1:],"run":os.environ["CLOVERWOOD_RUN_ROOT"],"tmp":os.environ["TMPDIR"],"dd":os.environ["CLOVERWOOD_DERIVED_DATA_PATH"]}))'
        out = self.finish(self.launch([sys.executable, "-B", "-c", code, "two words", "$(not-executed)"]), data="input kept\n")
        result = next(json.loads(s) for s in out.splitlines() if s.startswith('{'))
        self.assertEqual(result['args'], ['two words', '$(not-executed)'])
        self.assertEqual(result['stdin'], 'input kept\n')
        self.assertEqual(result['run'], str(self.run_root()))
        self.assertEqual(result['tmp'], str(self.run_root() / 'tmp') + '/')
        self.assertEqual(result['dd'], str(self.run_root() / 'DerivedData'))
        self.assertIn('cleanup=PASS', out)
        self.assertFalse(self.run_root().exists())
        self.assert_clear()

    def test_failure_exit_and_cleanup_preserved(self):
        out = self.finish(self.launch([BASH, '-c', 'echo error-message >&2; exit 42']), 42)
        self.assertIn('error-message', out)
        self.assertIn('command_exit=42 cleanup=PASS', out)
        self.assertFalse(self.run_root().exists())
        self.assert_clear()

    def test_missing_command_exits_127_and_releases_locks(self):
        self.assertIn('cleanup=PASS', self.finish(self.launch(['cw-no-such-command']), 127))
        self.assert_clear()

    def test_different_tmpdirs_and_repos_cannot_overlap(self):
        first, release = self.held()
        marker = self.base / 'must-not-run'
        env = self.env(self.b, run='second')
        env['CLOVERWOOD_REPO_NAME'] = 'other-repo'
        out = self.finish(self.launch([BASH, '-c', 'echo bad > "$1"', '_', str(marker)], env), 75)
        self.assertIn('reason=mac_busy', out)
        self.assertFalse(marker.exists())
        self.assertEqual((self.lock(self.system) / 'pid').read_text().strip(), str(first.pid))
        release.touch(); self.finish(first)
        self.finish(self.launch(['true'], self.env(self.b, run='after')))
        self.assert_clear(self.system, self.canonical, self.a, self.b)

    def test_lightweight_job_does_not_take_heavy_lock(self):
        first, release = self.held()
        self.finish(self.launch(['true'], self.env(self.b, run='light', heavy='0')))
        self.assertTrue(self.lock(self.system).exists())
        release.touch(); self.finish(first)

    def test_legacy_canonical_lock_blocks_and_rolls_back_common_lock(self):
        lock = self.lock(self.canonical); lock.mkdir(parents=True)
        (lock / 'pid').write_text('legacy-owner')
        self.finish(self.launch(['true']), 75)
        self.assertFalse(self.lock(self.system).exists())
        self.assertEqual((lock / 'pid').read_text(), 'legacy-owner')
        self.assertFalse(self.run_root().exists())

    def test_live_last_lock_releases_only_earlier_locks(self):
        lock = self.lock(self.a); lock.mkdir(parents=True)
        (lock / 'pid').write_text(str(os.getpid()))
        self.finish(self.launch(['true']), 75)
        self.assert_clear(self.system, self.canonical)
        self.assertEqual((lock / 'pid').read_text(), str(os.getpid()))

    def test_missing_owner_lock_never_auto_removed(self):
        self.lock(self.system).mkdir(parents=True)
        self.finish(self.launch(['true']), 75)
        self.assertTrue(self.lock(self.system).exists())

    def test_common_path_alias_and_trailing_slash_are_deduplicated(self):
        alias = self.base / 'alias'; alias.symlink_to(self.system, target_is_directory=True)
        env = self.env(alias)
        env['TMPDIR'] = str(alias) + '/'
        env['TEST_CANONICAL'] = str(self.system) + '/'
        out = self.finish(self.launch(['true'], env))
        self.assertIn('cleanup=PASS', out)
        self.assert_clear()

    def test_getconf_failure_falls_back_to_shared_tmp(self):
        self.finish(self.launch(['true'], self.env(TEST_GETCONF_FAIL='1')))
        self.assert_clear()

    def test_existing_run_id_is_not_overwritten_or_deleted(self):
        root = self.run_root(); root.mkdir(parents=True)
        (root / 'user-file').write_text('keep')
        self.finish(self.launch(['true']), 73)
        self.assertEqual((root / 'user-file').read_text(), 'keep')
        self.assert_clear()

    def test_same_run_id_lightweight_contention(self):
        first, release = self.held(self.env(heavy='0'))
        self.finish(self.launch(['true'], self.env(heavy='0')), 73)
        self.assertTrue(self.run_root().exists())
        release.touch(); self.finish(first)

    def test_group_termination_releases_only_after_child_stops(self):
        for sig, status in ((signal.SIGTERM, 143), (signal.SIGHUP, 129), (signal.SIGINT, 130)):
            with self.subTest(sig=sig):
                env = self.env(run='signal-' + str(sig))
                proc, release = self.held(env, name='signal-' + str(sig))
                os.killpg(proc.pid, sig)
                self.assertIn('cleanup=PASS', self.finish(proc, status))
                self.assertFalse(self.run_root(run=env['CLOVERWOOD_RUN_ID']).exists())
                self.assert_clear()

    def test_wrapper_only_term_holds_lock_while_foreground_child_runs(self):
        proc, release = self.held()
        proc.send_signal(signal.SIGTERM)
        time.sleep(0.1)
        self.assertIsNone(proc.poll())
        self.finish(self.launch(['true'], self.env(self.b, run='contender')), 75)
        release.touch(); self.finish(proc, 143)
        self.assert_clear()

    def test_sigkill_orphan_lock_is_recovered_when_owner_is_provably_dead(self):
        proc, release = self.held()
        proc.kill()
        proc.wait(timeout=3)
        out = self.finish(self.launch(['true'], self.env(self.b, run='after-crash')))
        self.assertIn('CLOVERWOOD_STALE_LOCK_RECOVERED', out)
        self.assertFalse(self.lock(self.system).exists())
        self.assertTrue(self.run_root().exists(), 'orphan run data is preserved for later bounded sweep')
        release.touch()
        out = self.finish(proc, -signal.SIGKILL)
        self.assertNotIn('CLOVERWOOD_CLEANUP_RECEIPT', out)

    def test_dead_pid_lock_with_extra_content_stays_fail_closed(self):
        lock = self.lock(self.system); lock.mkdir(parents=True)
        (lock / 'pid').write_text('2147483647')
        (lock / 'unexpected').write_text('keep')
        self.finish(self.launch(['true'], self.env(self.b, run='ambiguous-dead')), 75)
        self.assertTrue((lock / 'unexpected').exists())

    def test_invalid_canonical_root_never_creates_root_lock(self):
        out = self.finish(self.launch(['true'], self.env(TEST_CANONICAL='/')), 73)
        self.assertIn('reason=lock_parent_failed', out)
        self.assert_clear()

    def test_replaced_lock_pid_is_preserved_and_cleanup_fails(self):
        code = 'printf "%s" other-owner > ' + shlex.quote(str(self.lock(self.system) / 'pid'))
        out = self.finish(self.launch([BASH, '-c', code]), 86)
        self.assertIn('cleanup=FAIL', out)
        self.assertEqual((self.lock(self.system) / 'pid').read_text(), 'other-owner')
        self.assert_clear(self.canonical, self.a)

    def test_unexpected_lock_contents_are_not_recursively_deleted(self):
        path = self.lock(self.system) / 'foreign-file'
        self.finish(self.launch([BASH, '-c', 'echo keep > "$1"', '_', str(path)]), 86)
        self.assertEqual(path.read_text().strip(), 'keep')
        self.assertTrue(path.parent.exists())

    def test_removed_owned_lock_marker_is_not_a_setup_failure(self):
        path = self.lock(self.system)
        out = self.finish(self.launch([BASH, '-c', 'rm -- "$1/pid"', '_', str(path)]), 86)
        self.assertIn('cleanup=FAIL', out)
        self.assertTrue(path.is_dir(), 'lost ownership evidence must not authorize removal')
        self.assert_clear(self.canonical, self.a)

    def test_replaced_empty_lock_is_preserved(self):
        path = self.lock(self.system)
        code = 'rm -- "$1/pid" && rmdir "$1" && mkdir "$1"'
        self.finish(self.launch([BASH, '-c', code, '_', str(path)]), 86)
        self.assertTrue(path.is_dir(), 'replacement without owner evidence must remain blocked')

    def test_hardlinked_file_cleanup_preserves_external_permissions(self):
        outside = self.base / 'readonly-source'
        outside.write_text('keep source bytes')
        outside.chmod(0o400)
        inode = outside.stat().st_ino
        code = 'import os,sys; os.link(sys.argv[1], os.path.join(os.environ["CLOVERWOOD_RUN_ROOT"], "linked-source"))'
        self.finish(self.launch([sys.executable, '-B', '-c', code, str(outside)]))
        self.assertEqual(outside.read_text(), 'keep source bytes')
        self.assertEqual(outside.stat().st_ino, inode)
        self.assertEqual(outside.stat().st_nlink, 1)
        self.assertEqual(outside.stat().st_mode & 0o777, 0o400,
                         'cleanup must not chmod a source inode via its hard link')

    def test_readonly_nested_directories_clean_without_chmoding_files(self):
        outside = self.base / 'readonly-original'
        outside.write_text('keep')
        outside.chmod(0o400)
        code = ('import os,sys; from pathlib import Path; '
                'root=Path(os.environ["CLOVERWOOD_RUN_ROOT"]); '
                'parent=root/"no-access"; inner=parent/"nested"; inner.mkdir(parents=True); '
                'os.link(sys.argv[1],inner/"hardlink"); '
                'inner.chmod(0); parent.chmod(0)')
        self.finish(self.launch([sys.executable, '-B', '-c', code, str(outside)]))
        self.assertFalse(self.run_root().exists())
        self.assertEqual(outside.stat().st_mode & 0o777, 0o400)
        self.assertEqual(outside.read_text(), 'keep')

    def test_replaced_run_owner_is_not_deleted(self):
        self.finish(self.launch([BASH, '-c', 'echo other-owner > "$CLOVERWOOD_RUN_ROOT/.owner-pid"']), 86)
        self.assertEqual((self.run_root() / '.owner-pid').read_text().strip(), 'other-owner')

    def test_run_setup_failure_cleans_acquired_locks_and_owned_root(self):
        out = self.finish(self.launch(['true'], self.env(TEST_SETUP_FAIL='1')), 73)
        self.assertIn('reason=run_setup_failed', out)
        self.assertIn('cleanup=PASS', out)
        self.assert_clear(); self.assertFalse(self.run_root().exists())

    def test_symlinks_inside_run_do_not_change_external_files(self):
        outside = self.base / 'keep-readonly'; outside.mkdir()
        file = outside / 'master'; file.write_text('keep'); file.chmod(0o400)
        self.finish(self.launch([BASH, '-c', 'ln -s "$1" "$CLOVERWOOD_RUN_ROOT/link"', '_', str(outside)]))
        self.assertEqual(file.read_text(), 'keep')
        self.assertEqual(file.stat().st_mode & 0o777, 0o400)

    def test_symlink_run_parent_rejected(self):
        outside = self.base / 'outside'; outside.mkdir()
        (self.a / 'cloverwood-ci').symlink_to(outside, target_is_directory=True)
        self.finish(self.launch(['true']), 73)
        self.assertEqual(list(outside.iterdir()), [])

    def test_dangling_run_symlink_rejected(self):
        self.run_root().parent.mkdir(parents=True)
        self.run_root().symlink_to(self.base / 'missing')
        self.finish(self.launch(['true']), 73)
        self.assertTrue(self.run_root().is_symlink())

    def test_low_disk_never_runs_child_or_creates_locks(self):
        out = self.finish(self.launch(['true'], self.env(TEST_FREE_KIB='20971519')), 78)
        self.assertIn('reason=low_disk', out)
        self.assertNotIn('CLOVERWOOD_RUN_START', out)
        self.assert_clear(); self.assertFalse(self.run_root().exists())

    def test_exact_twenty_gib_is_allowed(self):
        self.finish(self.launch(['true'], self.env(TEST_FREE_KIB='20971520')))

    def test_invalid_configuration_rejected_before_execution(self):
        for key, value in (('CLOVERWOOD_RUN_ID', '../escape'), ('CLOVERWOOD_REPO_NAME', '../escape'),
                           ('CLOVERWOOD_MIN_FREE_GIB', '-1'), ('CLOVERWOOD_MIN_FREE_GIB', '1+1'),
                           ('CLOVERWOOD_EXCLUSIVE_MAC', 'maybe'), ('TMPDIR', 'relative/path')):
            with self.subTest(key=key, value=value):
                env = self.env(); env[key] = value
                out = self.finish(self.launch(['true'], env), 64)
                self.assertNotIn('CLOVERWOOD_RUN_START', out)
                self.assert_clear()

    def stale(self, name, pid=None):
        path = self.run_root().parent / name; path.mkdir(parents=True)
        if pid is not None: (path / '.owner-pid').write_text(str(pid))
        (path / 'temporary-data').write_text('data')
        old = time.time() - 172800; os.utime(path, (old, old))
        return path

    def test_stale_sweep_only_removes_dead_marked_same_repo_runs(self):
        dead = self.stale('old-dead', 99999999)
        alive = self.stale('old-alive', os.getpid())
        unknown = self.stale('old-unknown')
        malformed = self.stale('old-malformed', 'not-a-pid')
        self.finish(self.launch(['true']))
        self.assertFalse(dead.exists())
        for path in (alive, unknown, malformed): self.assertTrue(path.exists())

    def test_stale_sweep_is_suspended_when_heavy_lock_exists(self):
        dead = self.stale('old-dead', 99999999)
        self.lock(self.system).mkdir(parents=True)
        self.finish(self.launch(['true'], self.env(heavy='0')))
        self.assertTrue(dead.exists())
        self.assertTrue(self.lock(self.system).exists())

if __name__ == '__main__':
    unittest.main()
