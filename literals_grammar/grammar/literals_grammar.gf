abstract literals_grammar = TDM, Integers ** {

cat

Predicate_comment;
Sort_domain;
Sort_string;
Unknown;

fun

top : VpAction;
share_media : VpAction;
share_media_request : Unknown -> UsrRequest;
up : VpAction;
comment : Predicate;
comment_sys_answer : SysAnswer;
comment_user_answer : Sort_string -> UsrAnswer;
report_ended_ShareMedia_1 : SysAnswer -> SysReportEnded;
preconfirm_ShareMedia : SysAnswer -> SysYNQ;

unknown_comment : Unknown -> Sort_string;
mkUnknown : String -> Unknown;
}
