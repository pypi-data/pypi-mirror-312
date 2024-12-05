
ACTIVE_SERVICE_RUNNING_MODE_NONE = 0
ACTIVE_SERVICE_RUNNING_MODE_SQL = 1
ACTIVE_SERVICE_RUNNING_MODE_EXTERNALCALL = 2

ACTIVE_SERVICE_STATUS_CODE_INITIALIZING = 10
ACTIVE_SERVICE_STATUS_CODE_RUN = 20
ACTIVE_SERVICE_STATUS_CODE_REJECTING = 21
ACTIVE_SERVICE_STATUS_CODE_REJECTED = 22
ACTIVE_SERVICE_STATUS_CODE_REPETITIVE_CALL_REJECTED = 23
ACTIVE_SERVICE_STATUS_CODE_DB_CONNECTING = 50
ACTIVE_SERVICE_STATUS_CODE_DB_CONNECTED = 51
ACTIVE_SERVICE_STATUS_CODE_DB_STMT_OPEN = 52
ACTIVE_SERVICE_STATUS_CODE_SQL_EXECUTING = 54
ACTIVE_SERVICE_STATUS_CODE_SQL_EXECUTED = 55
ACTIVE_SERVICE_STATUS_CODE_SQL_RS_OPEN = 56
ACTIVE_SERVICE_STATUS_CODE_DB_CLOSED = 60
ACTIVE_SERVICE_STATUS_CODE_EXTERNALCALL_EXECUTING = 70
ACTIVE_SERVICE_STATUS_CODE_EXTERNALCALL_EXECUTED = 71
ACTIVE_SERVICE_STATUS_CODE_EXTERNALCALL_END = 72

ERROR_TYPE_SERVICE_EXCEPTION = 1001
ERROR_TYPE_METHOD_EXCEPTION = 1012  # error.py
ERROR_TYPE_EXTERNAL_CALL_EXCEPTION = 1014
ERROR_TYPE_TOO_MANY_FETCH = 1013
ERROR_TYPE_DB_CONNECTION_FAIL = 1015
ERROR_TYPE_DB_SQL_EXCEPTION = 1020
ERROR_TYPE_404 = 1022

REMOTE_CALL_TYPE_NONE = 0
REMOTE_CALL_TYPE_CUSTOM = 11
REMOTE_CALL_TYPE_HTTP = 12
REMOTE_CALL_TYPE_MONGODB = 17
REMOTE_CALL_TYPE_HTTPS = 18
REMOTE_CALL_TYPE_SAP = 19
REMOTE_CALL_TYPE_UNKNOWN_SQL_DATABASE = 21
REMOTE_CALL_TYPE_ORACLE = 22
REMOTE_CALL_TYPE_DB2 = 23
REMOTE_CALL_TYPE_MYSQL = 24
REMOTE_CALL_TYPE_POSTGRESQL = 25
REMOTE_CALL_TYPE_CUBRID = 26
REMOTE_CALL_TYPE_MSSQL = 27
REMOTE_CALL_TYPE_GHOST = 29
REMOTE_CALL_TYPE_MARIA = 30
REMOTE_CALL_TYPE_SOAP = 32
REMOTE_CALL_TYPE_SYBASE = 35
REMOTE_CALL_TYPE_INTERSYSTEMS_CACHEDB = 36
REMOTE_CALL_TYPE_REDIS = 37
REMOTE_CALL_TYPE_GOLDILOCKS = 38
REMOTE_CALL_TYPE_INFOMIX = 39
REMOTE_CALL_TYPE_SQLITE = 40
REMOTE_CALL_TYPE_TIBERO = 41
REMOTE_CALL_TYPE_CELERY = 42

DB_MESSAGE_TYPE_UNKNOWN = 0
DB_MESSAGE_TYPE_OPEN = 1
DB_MESSAGE_TYPE_CLOSE = 2
DB_MESSAGE_TYPE_COMMIT = 3
DB_MESSAGE_TYPE_ROLLBACK = 4
DB_MESSAGE_TYPE_AUTO_COMMIT_FAILED = 5

SQL_DEF_PSTMT_EXE_QRY = 5

X_DOMAIN_ID = "X-DOMAINID"
X_AGENT_ID = "X-AGENTID"
X_CALLTYPE_ID = "X-CALLTYPEID"

INCOMING_OUTGOING_TYPE_INCOMING = 0
INCOMING_OUTGOING_TYPE_OUTGOING = 1
INCOMING_OUTGOING_TYPE_SQL_OUTGOING = 2
INCOMING_OUTGOING_TYPE_NONE = 3

LOADED_CLASS_TREE_NODE_TYPE_NONE = 0
LOADED_CLASS_TREE_NODE_TYPE_PACKAGE = 1
LOADED_CLASS_TREE_NODE_TYPE_CLASS = 2
LOADED_CLASS_TREE_NODE_TYPE_METHOD = 3
