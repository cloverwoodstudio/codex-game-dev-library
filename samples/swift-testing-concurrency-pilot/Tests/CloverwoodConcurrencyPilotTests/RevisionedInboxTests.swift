import Testing
@testable import CloverwoodConcurrencyPilot

@Suite("Revisioned inbox: deterministic async behavior")
struct RevisionedInboxTests {
    @Test("latest response wins even if older result arrives later")
    func staleResponseIsRejected() async {
        let inbox = RevisionedInbox()
        let old = await inbox.begin()
        let new = await inbox.begin()

        #expect(!(await inbox.deliver(11, for: old)))
        #expect(await inbox.deliver(22, for: new))
        #expect(await inbox.current() == 22)
    }

    @Test("rejects an invalid token without overwriting current state")
    func invalidTicketDoesNotCommit() async {
        let inbox = RevisionedInbox()
        let token = await inbox.begin()
        #expect(!(await inbox.deliver(7, for: token + 1)))
        #expect(await inbox.current() == nil)
    }

    @Test("actor serializes concurrently initiated requests")
    func concurrentlyIssuedTokensAreUnique() async {
        let inbox = RevisionedInbox()
        async let left = inbox.begin()
        async let right = inbox.begin()
        let ids = await (left, right)
        #expect(ids.0 != ids.1)
        #expect(Set([ids.0, ids.1]) == Set([1, 2]))
    }

    @Test("a task cancelled before delivery cannot publish")
    func cancellationPreventsPublish() async {
        let inbox = RevisionedInbox()
        let ticket = await inbox.begin()

        let worker = Task {
            withUnsafeCurrentTask { task in task?.cancel() }
            return await inbox.deliver(99, for: ticket)
        }

        #expect(!(await worker.value))
        #expect(await inbox.current() == nil)
    }
}
