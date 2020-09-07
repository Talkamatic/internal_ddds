abstract small_grammar = {

cat

User;
UsrYesNo;
UsrRequest;
UsrAnswer;
NpAction;
Sort_city;

fun

userNpActionRequest : NpAction -> UsrRequest;
userRequest : UsrRequest -> User;
userYesNoRequest : UsrYesNo -> UsrRequest -> User;
userYesNo : UsrYesNo -> User;
userYes, userNo : UsrYesNo;
userAnswer : UsrAnswer -> User;

top : NpAction;
olearys : NpAction;
city_user_answer : Sort_city -> UsrAnswer;
public : Sort_city;

placeholder_city0 : Sort_city;
placeholder_city1 : Sort_city;
placeholder_city2 : Sort_city;
placeholder_city3 : Sort_city;
placeholder_city4 : Sort_city;
placeholder_city5 : Sort_city;
placeholder_city6 : Sort_city;
placeholder_city7 : Sort_city;
placeholder_city8 : Sort_city;
placeholder_city9 : Sort_city;

}
