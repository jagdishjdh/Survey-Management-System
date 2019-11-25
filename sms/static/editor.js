  function crtsec(){
    var sec_div = document.createElement("div");
    var new_line = document.createElement("hr");
    var title = document.createElement("input");
    var desc = document.createElement("input");
    var nameplate = document.createElement("p");
    var qlist = document.createElement("ol");
    var copybtn = document.createElement("button");
    var rmbtn = document.createElement("button");

    var rmtext = document.createTextNode("remove");
    var copytext = document.createTextNode("Copy");

    sec_div.setAttribute("class","sec_div");
    new_line.setAttribute("class","myhr");
    title.setAttribute("class","sec_ttl");
    desc.setAttribute("class","sec_desc");
    nameplate.setAttribute("class","sec_plate");


    title.setAttribute("value","section title");
    desc.setAttribute("value","section description (optional)");
    nameplate.innerHTML = "Section";

    copybtn.setAttribute("class", "removebtn");
    copybtn.setAttribute("onclick", "Copy_sec(this)");
    rmbtn.setAttribute("class", "removebtn");
    rmbtn.setAttribute("onclick", "Delete_sec(this)");

    var secoptn = document.getElementById("selected_sec");
    var optnum = secoptn.length + 1;
    var option = document.createElement("option");
    option.text = optnum;
    secoptn.appendChild(option);
  

    copybtn.appendChild(copytext);
    rmbtn.appendChild(rmtext);

    sec_div.appendChild(new_line);
    sec_div.appendChild(nameplate);
    sec_div.appendChild(title);
    sec_div.appendChild(copybtn);
    sec_div.appendChild(rmbtn);
    sec_div.appendChild(desc);
    sec_div.appendChild(qlist);

    var node = document.createElement("LI");
    node.appendChild(sec_div);
    document.getElementById("seclist").appendChild(node);


  }
  function Delete_sec(button) {
      var parent = button.parentNode;
      var grand_father = parent.parentNode;
      var gg_father = grand_father.parentNode;
      gg_father.removeChild(grand_father);

      var x = document.getElementById("selected_sec");      //remove one option from select sec

      if (x.length > 0) {
        x.remove(x.length-1);
      }else{}     
}

  function Copy_sec(button) {
    var parent = button.parentNode;
    var clone = parent.cloneNode(true);

    var secid = clone.querySelector('.sec_id');
    if(clone.contains(secid)){
       secid.remove();
       var secnum = clone.querySelector('.sec_num');
       secnum.remove();
    }  else{}

    var node = document.createElement("LI");
    node.appendChild(clone);
    document.getElementById("seclist").appendChild(node);

    var secoptn = document.getElementById("selected_sec");    // add a option to selcte_sec
    var optnum = secoptn.length + 1;
    var option = document.createElement("option");
    option.text = optnum;
    secoptn.appendChild(option);
  }

  function crtQ() {
    var addtosec = document.getElementById("selected_sec").selectedIndex ;
    var currentsec = document.getElementsByClassName("sec_div")[addtosec];
    var secqlist = currentsec.getElementsByTagName("ol")[0];
  
    var my_div = document.createElement("div");
    var ans_div = document.createElement("div");
    var rmbtn = document.createElement("button");
    var copybtn = document.createElement("button");
    var askQ = document.createElement("input");
    var ans = document.createElement("input");
    var label = document.createElement("label");
    var rcheckbox = document.createElement("input");
    var round = document.createElement("span");
  
    var textarr = ["Short Ans ","Paragraph","Multiple choice",
          "Checkboxes","Drop-down","File upload","linear scale",
          "multiple choice grid","tick box grid","Date","Time"];
  
    //Create and append select list
    var qtypeselect = document.createElement("select");
    my_div.appendChild(qtypeselect);
  
    //Create and append the options
    for (var i = 0; i < textarr.length; i++) {
        var option = document.createElement("option");
        option.text = textarr[i];
        qtypeselect.appendChild(option);
    }
  
    my_div.setAttribute("class", "oneq");               
    ans_div.setAttribute("class", "textans_div");               
    rmbtn.setAttribute("class", "removebtn");
    rmbtn.setAttribute("onclick", "DeleteQ(this)");
    copybtn.setAttribute("class", "removebtn");
    copybtn.setAttribute("onclick", "CopyQ(this)");
    qtypeselect.setAttribute("onchange", "modifyQ(this)");
    qtypeselect.setAttribute("class", "Qtype");
    askQ.setAttribute("class", "mainQ");
    askQ.setAttribute("value", "write your question here");
    ans.setAttribute("value", " short ans here");
    ans.setAttribute("class", "textans");
    ans.setAttribute("type", "text");
    ans.setAttribute("disabled", true);
  
    label.setAttribute("class","switch" )
    rcheckbox.setAttribute("type","checkbox" )
    rcheckbox.setAttribute("class","toggle" )
    round.setAttribute("class","slider round" )
    
    var rmtext = document.createTextNode("remove");
    var copytext = document.createTextNode("Copy");
    var requiretext = document.createTextNode("Require");
    // requiretext.setAttribute("class", "requiretext");
  
  
    label.appendChild(rcheckbox);
    label.appendChild(round);
  
    rmbtn.appendChild(rmtext);
  
    my_div.appendChild(rmbtn);
    my_div.appendChild(copybtn);
    my_div.appendChild(requiretext);
  
    my_div.appendChild(label);
  
    copybtn.appendChild(copytext);
    my_div.appendChild(askQ);
    ans_div.appendChild(ans);
    my_div.appendChild(ans_div);
      
    var node = document.createElement("LI");
    node.appendChild(my_div);
    secqlist.appendChild(node);
  }
  function DeleteQ(button) {
      var parent = button.parentNode;
      var grand_father = parent.parentNode;
      var gg_father = grand_father.parentNode;
      gg_father.removeChild(grand_father);
    }
  function CopyQ(button) {
    var addtosec = document.getElementById("selected_sec").selectedIndex ;
    var target_sec = document.getElementsByClassName("sec_div")[addtosec];
    var secqlist = target_sec.querySelector("ol");

    var parent = button.parentNode;
    var clone = parent.cloneNode(true);

    var qtype_index = parent.getElementsByClassName("Qtype")[0].selectedIndex;
  
    var qtype2 = clone.getElementsByClassName("Qtype")[0];
    qtype2.options[qtype_index].selected = true;

    var node = document.createElement("LI");
    node.appendChild(clone);
    secqlist.appendChild(node);
  }
  function modifyQ(button){
    var ind = button.selectedIndex;
    var parent = button.parentNode;
  
    if (ind ==0 || ind ==1) {
        var ansdiv = parent.querySelector('.textans_div');
        if(parent.contains(ansdiv)){
          var ansinfld =ansdiv.querySelector('input');
          if(ind ==0) { ansinfld.setAttribute("value", "short answer here"); } 
          else { ansinfld.setAttribute("value", "long answer here"); } 
        }
        else{
            var ansdivoptn = parent.querySelector("div:not(.textans_div)");
            ansdivoptn.remove();
  
          var ans_newdiv = document.createElement("div");
          ans_newdiv.setAttribute("class", "textans_div");                
  
          var shortans = document.createElement("input");
          shortans.setAttribute("class", "textans");                
          shortans.setAttribute("type", "text");
          shortans.setAttribute("disabled", true);                
          if(ind == 0){ shortans.setAttribute("value", "short answer here"); }
          if(ind==1) {      shortans.setAttribute("value", "long answer here"); }
          
          ans_newdiv.appendChild(shortans);
          parent.appendChild(ans_newdiv);
      }
    }
  
      else if(ind >= 2 && ind <=4) {
        var ansdiv = parent.querySelector('.options_div');
        if(parent.contains(ansdiv)){}
        else{
            var ansdiv2 =parent.querySelector("div:not(.options_div)");
            ansdiv2.remove();
  
          var ans_newdiv = document.createElement("div");
          var optnlist = document.createElement("ul");
          var optnlist2 = document.createElement("ul");
          var option1 = document.createElement("li");
          var extraoptn = document.createElement("li");
          var optnval = document.createElement("input");
          var optbtn = document.createElement("button");
          var otherbtn = document.createElement("button");
  
          var addtxt = document.createTextNode("Add new Option");
          var othertxt = document.createTextNode("Other");
          var ortxt = document.createTextNode("  OR  ");
  
          ans_newdiv.setAttribute("class", "options_div");                
          optnval.setAttribute("class", "option");                
          optnval.setAttribute("type", "text");               
          optnval.setAttribute("value", "Option-1");
  
          optbtn.setAttribute("onclick", "addopt(this)");               
          otherbtn.setAttribute("onclick", "addother(this)");
  
          optbtn.appendChild(addtxt);
          otherbtn.appendChild(othertxt);
          extraoptn.appendChild(optbtn);
          extraoptn.appendChild(ortxt);
          extraoptn.appendChild(otherbtn);
  
          option1 .appendChild(optnval);
          optnlist.appendChild(option1);                    
          optnlist2.appendChild(extraoptn);
          ans_newdiv.appendChild(optnlist);
          ans_newdiv.appendChild(optnlist2);
          parent.appendChild(ans_newdiv);
        }
      }
      else if(ind == 5){
          var olderans_div =parent.querySelector("div");
          olderans_div.remove();
  
        var ans_newdiv = document.createElement("div");
        ans_newdiv.setAttribute("class", "file_div");
  
        var file_in = document.createElement("input");
        var note = document.createTextNode(" user will upload a file here ");
        file_in.setAttribute("type", "file");
        file_in.setAttribute("class", "file_input");
        file_in.setAttribute("disabled", true);
  
        ans_newdiv.appendChild(file_in);
        ans_newdiv.appendChild(note);
        parent.appendChild(ans_newdiv);
      }
      else if(ind == 6){
          var olderans_div =parent.querySelector("div");
          olderans_div.remove();
  
        var ans_newdiv = document.createElement("div");
        ans_newdiv.setAttribute("class", "scale_div");
  
        var start = document.createTextNode(" start-label:- ");
        var end = document.createTextNode(" end-label:- ");
        var to = document.createTextNode(" to ");
        var start_in = document.createElement("input");
        var end_in = document.createElement("input");
  
        var startarr = [0,1];
        var endarr = [2,3,4,5,6,7,8,9,10];
  
        var select_start = document.createElement("select");
        var select_end = document.createElement("select");
  
        for (var i = 0; i < startarr.length; i++) {
            var option = document.createElement("option");
            option.text = startarr[i];
            select_start.appendChild(option);
        }
        for (var i = 0; i < endarr.length; i++) {
            var option = document.createElement("option");
            option.text = endarr[i];
            select_end.appendChild(option);
        }
  
        ans_newdiv.appendChild(select_start);
        ans_newdiv.appendChild(to);                   
        ans_newdiv.appendChild(select_end);
        ans_newdiv.appendChild(start);
        ans_newdiv.appendChild(start_in);
        ans_newdiv.appendChild(end);
        ans_newdiv.appendChild(end_in);
        parent.appendChild(ans_newdiv);
      }
  
      else if(ind == 7 || ind ==8) {
        var ansdiv = parent.querySelector('.RCoptions_div');
        if(parent.contains(ansdiv)){}
        else{
            var ansdiv2 =parent.querySelector("div:not(.RCoptions_div)");
            ansdiv2.remove();
  
          var ans_newdiv = document.createElement("div");
          ans_newdiv.setAttribute("class", "RCoptions_div");  
          var rowtxth = document.createElement("h4");
          var coltxth = document.createElement("h4");
          var RowoptnList = document.createElement("ul");
          var RowoptnList2 = document.createElement("ul");
          var option1 = document.createElement("li");
          var extraoptn = document.createElement("li");
          var optnval = document.createElement("input");
          var optbtn = document.createElement("button");
  
          var addtxt = document.createTextNode("Add new Option");
          var othertxt = document.createTextNode("Other");
          var rowtxt = document.createTextNode("Rows:-");
          var coltxt = document.createTextNode("Columns:-");
  
          rowtxth .appendChild(rowtxt);
          coltxth .appendChild(coltxt);
  
          optnval.setAttribute("class", "option");                
          optnval.setAttribute("type", "text");               
          optnval.setAttribute("value", "Option-1");
  
          optbtn.setAttribute("onclick", "addopt(this)");               
  
          optbtn.appendChild(addtxt);
          extraoptn .appendChild(optbtn);
  
          option1 .appendChild(optnval);
          RowoptnList.appendChild(option1);                   
          RowoptnList2.appendChild(extraoptn);
    var ColoptnList = document.createElement("ul");
    var ColoptnList2 = document.createElement("ul");
    var option1 = document.createElement("li");
    var extraoptn = document.createElement("li");
    var optnval = document.createElement("input");
    var optbtn = document.createElement("button");
  
    var addtxt = document.createTextNode("Add new Option");
    var othertxt = document.createTextNode("Other");
  
    optnval.setAttribute("class", "option");                
    optnval.setAttribute("type", "text");               
    optnval.setAttribute("value", "Option-1");
  
    optbtn.setAttribute("onclick", "addopt(this)");               
  
    optbtn.appendChild(addtxt);
    extraoptn .appendChild(optbtn);
  
    option1 .appendChild(optnval);
    ColoptnList.appendChild(option1);                   
    ColoptnList2.appendChild(extraoptn);
  
          ans_newdiv.appendChild(rowtxth);
          ans_newdiv.appendChild(RowoptnList);
          ans_newdiv.appendChild(RowoptnList2);
          ans_newdiv.appendChild(coltxth);
          ans_newdiv.appendChild(ColoptnList);
          ans_newdiv.appendChild(ColoptnList2);
          parent.appendChild(ans_newdiv);
        }
      }
  
      else if(ind==9){
          var olderans_div =parent.querySelector("div");
          olderans_div.remove();
  
        var ans_newdiv = document.createElement("div");
        ans_newdiv.setAttribute("class", "date_div");
  
        var date_in = document.createElement("input");
        date_in.setAttribute("type", "date");
  
        ans_newdiv.appendChild(date_in);
        parent.appendChild(ans_newdiv);
      }
      else if(ind==10){
          var olderans_div =parent.querySelector("div");
          olderans_div.remove();
  
        var ans_newdiv = document.createElement("div");
        ans_newdiv.setAttribute("class", "time_div");
  
        var time_in = document.createElement("input");
        time_in.setAttribute("type", "time");
  
        ans_newdiv.appendChild(time_in);
        parent.appendChild(ans_newdiv);
      }
      else{}
    }
  
  function addopt(button){
    var parent = button.parentNode;
    var grand_father = parent.parentNode.previousSibling;
    var optnindex = grand_father.childElementCount + 1;
  
    var option2 = document.createElement("li");
    var optnval = document.createElement("input");
    var remove_opt = document.createElement("button");
    var remove_txt = document.createTextNode(" Remove Option");
  
    optnval.setAttribute("class", "option");                
    optnval.setAttribute("type", "text");               
    optnval.setAttribute("value","Option-" + optnindex);
    remove_opt.setAttribute("onclick","remove_opt(this)");
  
    remove_opt.appendChild(remove_txt);
    option2 .appendChild(optnval);
    option2 .appendChild(remove_opt);
  
    grand_father.appendChild(option2);
  }
  
  function addother(button){
      var parent = button.parentNode;
      var grand_father = parent.parentNode;
      if(grand_father.childElementCount > 1){}
  
      else{
      var othroptn = document.createElement("li");
      var optnval = document.createElement("input");
      var remove_opt = document.createElement("button");
      var remove_txt = document.createTextNode(" Remove Option");
  
      optnval.setAttribute("class", "otheroptn");               
      optnval.setAttribute("type", "text");               
      optnval.setAttribute("value","Other ...");
      optnval.setAttribute("disabled",true);
      remove_opt.setAttribute("onclick","remove_opt(this)");
  
      remove_opt.appendChild(remove_txt);
      othroptn.appendChild(optnval);
      othroptn.appendChild(remove_opt);
  
      grand_father.insertBefore(othroptn, grand_father.lastChild);
    }
  }
  function remove_opt(button) {
      var parent = button.parentNode;
      var grand_father = parent.parentNode;
      grand_father.removeChild(parent);
    }
 
