
<script>
var carName1 = "Volvo XC60";
var carName2 = 'Volvo XC60';
var answer1 = "It's alright";
var answer2 = "He is called 'Johnny'";
var answer3 = 'He is called "Johnny"';

document.getElementById("demo").innerHTML =
carName1 + "<br>" + 
carName2 + "<br>" + 
answer1 + "<br>" + 
answer2 + "<br>" + 
answer3;
</script>

<script>
function myFunction() {
    var str = "a,b,c,d,e,f";
    var arr = str.split(",");
    document.getElementById("demo").innerHTML = arr[0];
}
</script>
