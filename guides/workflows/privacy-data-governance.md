# Privacy and player-data governance

Reviewed: 2026-08-29

This is an engineering workflow, not legal advice. Applicable law varies by audience and territory; obtain qualified review where required. The durable rule is to know every data flow before shipping it.

## Data inventory

For each field record source, purpose, controller/processor, destination, identity link, consent or other basis, retention, deletion/export path, security class, audience/age implications and every third-party SDK involved. Include crash reports, diagnostics, gameplay events, saves, chat, voice, UGC, support tickets, device IDs and platform services.

Data processed only on-device has different disclosure implications from data transmitted off-device, but still needs security and deletion behavior. Never infer that an SDK collects nothing: verify its configuration, network traffic and current vendor documentation.

## Minimize by design

- collect only what answers a named product, safety or reliability need;
- prefer coarse, anonymous or short-lived identifiers;
- keep unrestricted text, voice, screenshots and save contents out of telemetry;
- separate optional analytics/marketing from essential service operation;
- use bounded retention and automatic deletion;
- provide safe defaults when consent is absent or withdrawn;
- avoid dark patterns that pressure acceptance.

## Store declarations

Google Play requires developers to declare collection, sharing and protection practices, including third-party SDK behavior. Apple requires App Privacy details for app and update submissions and explicitly recognizes gameplay content such as saves, matchmaking and UGC. Store labels, privacy policy, runtime consent and actual network behavior must agree.

## Verification

Build a clean-account test: first launch, decline/accept choices, gameplay, crash, support, export and deletion. Inspect outbound traffic per platform/configuration. Verify deletion through downstream processors and backups according to policy. Re-audit when adding an SDK, data field, region, child audience, social feature or AI integration.

## Sources

- Google Play Data safety: https://support.google.com/googleplay/android-developer/answer/10787469
- Apple App Privacy details: https://developer.apple.com/app-store/app-privacy-details/
- Apple user privacy and data use: https://developer.apple.com/app-store/user-privacy-and-data-use/
