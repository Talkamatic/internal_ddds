concrete literals_grammar_eng of literals_grammar = TDM_eng, Integers_eng ** open Utils_eng in {

lin

top = (mkverb "main menu" "main menu" "main menu");
share_media = (mkverb "share my film" "share my film" "share my film"|mkverb "share my film on twitter" "share my film on twitter" "share my film on twitter"|mkverb "share on twitter" "share on twitter" "share on twitter"|mkverb "share" "share" "share");
share_media_request comment = ss ("share on twitter" ++ comment.s);
up = (mkverb "go back" "go back" "go back");
comment = ss "What comment would you like to share";
comment_sys_answer = answer ("_placeholder_0_");
comment_user_answer string = string;
comment_propositional_usr_answer string = string;
comment_sortal_usr_answer string = string;
report_ended_ShareMedia_1 comment = ss ("media shared!");
preconfirm_ShareMedia comment = ss ("post on Facebook" ++ comment.alt);

unknown_comment unknown = unknown;
mkUnknown string = string;
}
