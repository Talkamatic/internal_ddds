concrete small_grammar_eng of small_grammar = {

oper

SS : Type = {s : Str};
ss : Str -> SS;
ss str = {s = str};


lincat

User = SS;
UsrYesNo = SS;


lin

userNpActionRequest act = act;
userRequest req = req;
userYesNoRequest yn req = ss (yn.s ++ req.s);
userYesNo yn = yn;
userYes = ss ("yes");
userNo = ss ("no");

top = ss "main menu";
olearys = ss ("oleary" ++ "'s");
public = ss ("public");
city_user_answer answer = answer;
userAnswer answer = answer;

placeholder_city0 = ss "_nl_placeholder_city0_";
placeholder_city1 = ss "_nl_placeholder_city1_";
placeholder_city2 = ss "_nl_placeholder_city2_";
placeholder_city3 = ss "_nl_placeholder_city3_";
placeholder_city4 = ss "_nl_placeholder_city4_";
placeholder_city5 = ss "_nl_placeholder_city5_";
placeholder_city6 = ss "_nl_placeholder_city6_";
placeholder_city7 = ss "_nl_placeholder_city7_";
placeholder_city8 = ss "_nl_placeholder_city8_";
placeholder_city9 = ss "_nl_placeholder_city9_";

}
