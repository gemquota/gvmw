"""Exception types. Every refusal is also recorded in the governance log by the
component that raises it (the exception is the in-process signal, the log entry
is the durable record)."""


class MedBError(Exception):
    pass


class AppendOnlyViolation(MedBError):
    pass


class NotAuthorized(MedBError):
    """Actor lacks authority for the requested operation."""


class PermissionDenied(MedBError):
    """Permission closure over a derivation path failed (Principle 6)."""


class CapabilitySuspended(MedBError):
    def __init__(self, primitive: str, interface: str, record_id: str | None):
        super().__init__(f"capability '{primitive}' is suspended (record {record_id}); "
                         f"interface '{interface}' refused")
        self.primitive = primitive
        self.interface = interface
        self.record_id = record_id


class SuspensionNotLiftable(MedBError):
    pass


class CharterResolutionUnavailable(MedBError):
    pass


class ConstitutionalProhibition(MedBError):
    pass


class PackageExpired(MedBError):
    pass


class UnknownClaim(MedBError):
    pass
