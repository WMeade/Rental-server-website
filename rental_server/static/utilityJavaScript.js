class Utils{
    static disableButton(){
        var radiobutton = document.getElementById("radiobutton");
        if (radiobutton.checked){
          document.getElementById("editbutton").disabled = false;
          document.getElementById("editbuttontwo").disabled = false;
        }
    }
}
