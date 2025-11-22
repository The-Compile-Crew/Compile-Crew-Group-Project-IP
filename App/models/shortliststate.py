#ignore comment

from App.models.shortlist import ShortlistState, DecisionStatus


# Applied State

class AppliedState(ShortlistState):
    def advance(self, context):
        # TODO: implement transition to ShortlistedState
        pass

    def accept(self, context):
        # TODO: invalid action from Applied
        pass

    def reject(self, context):
        # TODO: implement transition to RejectedState
        pass

    def get_status(self):
        # TODO: return DecisionStatus.applied
        pass


# Shortlisted State

class ShortlistedState(ShortlistState):
    def advance(self, context):
        # TODO: implement transition to AcceptedState
        pass

    def accept(self, context):
        # TODO: implement transition to AcceptedState
        pass

    def reject(self, context):
        # TODO: implement transition to RejectedState
        pass

    def get_status(self):
        # TODO: return DecisionStatus.shortlisted
        pass


# Accepted State

class AcceptedState(ShortlistState):
    def advance(self, context):
        # TODO: no-op or raise exception
        pass

    def accept(self, context):
        # TODO: already accepted
        pass

    def reject(self, context):
        # TODO: invalid action
        pass

    def get_status(self):
        # TODO: return DecisionStatus.accepted
        pass

# Rejected State

class RejectedState(ShortlistState):
    def advance(self, context):
        # TODO: invalid action
        pass

    def accept(self, context):
        # TODO: invalid action
        pass

    def reject(self, context):
        # TODO: already rejected
        pass

    def get_status(self):
        # TODO: return DecisionStatus.rejected
        pass

# Note: The above methods contain TODO comments indicating where the actual implementation logic should go.
# All TODOs to either be done by me or members we are still deciding