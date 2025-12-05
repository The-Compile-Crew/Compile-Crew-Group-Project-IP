# Model tests
from .test_models.test_user_models import *
from .test_models.test_position_models import *
from .test_models.test_shortlist_models import *

# Controller tests
from .test_controllers.test_user_controllers import *
from .test_controllers.test_position_controllers import *
from .test_controllers.test_auth_controllers import *
from .test_controllers.test_shortlist_controllers import *

# View tests
from .test_views import *

# Integration tests
from .test_integration import *
from .test_integration.test_staff_workflow import *

