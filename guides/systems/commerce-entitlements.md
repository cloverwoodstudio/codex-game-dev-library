# Purchases, DLC and entitlement lifecycle

Reviewed: 2026-08-29

Commerce is a distributed transaction among player, storefront, client and backend. The purchase UI is not proof of ownership; the canonical entitlement follows verified platform state.

## Catalog contract

Each offer has stable internal/platform product IDs, type (consumable, durable, subscription, DLC), localized storefront-owned price display, contents, eligibility, availability, version, refund/revocation behavior, age/territory rules and support playbook. Never hardcode or construct a price string when the platform provides it.

## Safe transaction

`intent → platform UI → pending/completed/cancelled result → backend verification → idempotent grant → acknowledgement/consumption → receipt/audit → reconciliation`

Treat callbacks and server notifications as repeatable and out of order. Store unique transaction/purchase tokens, validate product/account/state, grant once atomically and reconcile after crashes or offline completion. Google recommends backend verification and explicitly forbids granting while a purchase is pending; Apple StoreKit supports verified transactions and server APIs/notifications.

## Entitlements

Separate financial transaction records from the player's current entitlement set. Handle restore, refund, chargeback, subscription renewal/expiry, family/device changes, revoked DLC and two-platform accounts. Do not delete consumed-gameplay results blindly after a refund; define a fraud, debt or future-access policy with support review.

## Ethical and operational gates

Show exact contents and probabilities where applicable and required, provide purchase confirmation and spending/parental controls, avoid coercive timers and protect minors. Test sandbox purchases, pending approval, interruption after payment, duplicate notification, wrong account, refund, offline restore and service outage.

## Sources

- Google Play Billing security: https://developer.android.com/google/play/billing/security
- Google Play Billing integration: https://developer.android.com/google/play/billing/integrate
- Apple StoreKit In-App Purchase: https://developer.apple.com/documentation/storekit/in-app-purchase
- Apple sandbox purchase testing: https://developer.apple.com/documentation/storekit/testing-in-app-purchases-with-sandbox
- Steam microtransactions: https://partner.steamgames.com/doc/features/microtransactions
