/// Small, intentionally isolated production-pattern fixture.
/// Revision tokens prevent an older async response from overwriting a newer one.
public actor RevisionedInbox {
    private var generation = 0
    private var latestValue: Int?

    public init() {}

    /// Returns a token for a newly started logical request.
    public func begin() -> Int {
        generation += 1
        return generation
    }

    /// Only the current non-cancelled request can publish a result.
    @discardableResult
    public func deliver(_ value: Int, for token: Int) -> Bool {
        guard token == generation, !Task.isCancelled else { return false }
        latestValue = value
        return true
    }

    public func current() -> Int? { latestValue }
}
