#ignore comment

from App.models.shortlist import ShortlistState, DecisionStatus


# Applied State

class AppliedState(ShortlistState):
    def advance(self, context):
        # TODO: implement transition to ShortlistedState
         context.state = ShortlistedState()
        pass

    def accept(self, context):
        # TODO: invalid action from Applied
         raise Exception("Cannot accept. Candidate must be shortlisted first.")
        pass

    def reject(self, context):
        # TODO: implement transition to RejectedState
         context.state = RejectedState()
        pass

    def get_status(self):
        # TODO: return DecisionStatus.applied
        return DecisionStatus.applied
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
        raise Exception("Already accepted, cannot advance further")

    def accept(self, context):
        raise Exception("Already accepted")

    def reject(self, context):
        raise Exception("Cannot reject after acceptance")

    def get_status(self):
        return DecisionStatus.accepted
    
# Rejected State

class RejectedState(ShortlistState):
    def advance(self, context):
        raise Exception("Cannot advance. The Shortlist entry is already rejected")
        
    def accept(self, context):
        raise Exception("Cannot accept. The Shortlist entry is already rejected")

    def reject(self, context):
        raise Exception("Shortlist entry is already rejected")

    def get_status(self):
        return DecisionStatus.rejected

# Note: The above methods contain TODO comments indicating where the actual implementation logic should go.
# All TODOs to either be done by me or members we are still deciding
