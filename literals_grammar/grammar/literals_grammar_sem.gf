concrete literals_grammar_sem of literals_grammar = TDM_sem, Integers_sem ** open Utils_sem in {

lincat

Predicate_comment = SS;
Sort_domain = SS;
Sort_string = SS;
Unknown = SS;

lin

top = pp "top";
share_media = pp "share_media";
share_media_request comment = request (pp "share_media") (ss ("\"" ++ comment.s ++ "\""));
up = pp "up";
comment = pp "comment";
comment_sys_answer = pp "comment" (ss "_STR0_");
comment_user_answer string = string;
report_ended_ShareMedia_1 comment = report_ended "ShareMedia" (list comment);
preconfirm_ShareMedia comment = ask_preconfirm "ShareMedia" (list comment);

unknown_comment unknown = ss ("\"" ++ unknown.s ++ "\"");
mkUnknown string = ss string.s;
}
