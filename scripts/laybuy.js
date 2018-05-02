// Server object that will contain the callable methods
var server = {};
    
// Create Global couner
var g_counter = 0;

//
// Makes an AJAX request to a local server function w/ optional arguments
//
// functionName: the name of the server's AJAX function to call
// opt_argv: an Array of arguments for the AJAX function
//
function Request(function_name, opt_argv) {

	if (!opt_argv)
    opt_argv = new Array();

  // Find if the last arg is a callback function; save it
  var callback = null;
  var len = opt_argv.length;
  if (len > 0 && typeof opt_argv[len-1] == 'function') {
    callback = opt_argv[len-1];
    opt_argv.length--;
  }
  var async = (callback != null);

  // Encode the arguments in to a URI
  var query = 'action=' + encodeURIComponent(function_name);
  for (var i = 0; i < opt_argv.length; i++) {
    var key = 'arg' + i;
    var val = JSON.stringify(opt_argv[i]);
    query += '&' + key + '=' + encodeURIComponent(val);
  }
  query += '&time=' + new Date().getTime(); // IE cache workaround

  // Create an XMLHttpRequest 'GET' request w/ an optional callback handler
  var req = new XMLHttpRequest();
  req.open('GET', '/rpc?' + query, async);

  if (async) {
    req.onreadystatechange = function() {
      if(req.readyState == 4 && req.status == 200) {
        var response = null;
        try {
         response = JSON.parse(req.responseText);
        } catch (e) {
         response = req.responseText;
        }
        callback(response);
      }
    }
  }

  // Make the actual request
  req.send(null);
}

// Adds a stub function that will pass the arguments to the AJAX call
function InstallFunction(obj, functionName) {
  obj[functionName] = function() { Request(functionName, arguments); }
}
  
//Handy "macro"
function $(id) {
  return document.getElementById(id);
}
    
function updateselected() {
	document.getElementById("currcontract").value=event.currentTarget.id
//	alert(event.currentTarget.id)
//	alert(document.getElementById("currcontract").value)
//	alert(event.currentTarget.id);
//	document.cc.innerHTML = event.currentTarget.id;-->
//	document.getElementById("f1").submit();-->
}

function submitform() {
	document.getElementById("f1").submit();
//	document.forms[0].submit();-->
}

function displaymessage() {
	alert("Hello World!");
}

function AddItem() {
	//Go get the number of Items
	var trrows = document.getElementById('bodyItem').childNodes;
	
	//Clone the first Item - Changed the other rows to trItemO, want to skip until the last record
	var trnew = document.getElementById('trItem').cloneNode(true);
	
	//Now loop thru the first line of children, drill deeper for each on found
	var trChild = trnew.childNodes;
	for (var i=0;i<trChild.length;i++) {	
		if (trChild[i].nodeName == 'TD') {
			var trChild2 = trChild[i].childNodes; //Go one level deeper
			for (var i2=0;i2<trChild2.length;i2++) {
				var theId = trChild2[i2].id;
				if (theId) {
					trChild2[i2].id = theId + trrows.length; //Add counter to id!!!!
				}	

				//Clear ALL the fields values
				trChild2[i2].value = '';
				
				//Adjust the HREF attributes as follows
				if (trChild2[i2].name == 'bAddDel') {	
					trChild2[i2].value = 'Remove';
					trChild2[i2].onclick = removeItem;
					trChild2[i2].style.fontSize = '8px';
				}				
			}
		}
	}
	
	//Add the new record to the document
	document.getElementById("bodyItem").appendChild(trnew);
    
	//return false;
}

function AddPayment() {
	//Go get the number of Payments
	var trrows = document.getElementById('bodyPaym').childNodes;
	
//	document.getElementById('trPaym').('datei').removeClass('hasDatepicker').datepicker();
	
	//Clone the first Payment
	var trnew = document.getElementById('trPaym').cloneNode(true);

	//Now loop thru the first line of children, drill deeper for each on found
	var trChild = trnew.childNodes;
	for (var i=0;i<trChild.length;i++) {	
		if (trChild[i].nodeName == 'TD') {
			var trChild2 = trChild[i].childNodes; //Go one level deeper
			for (var i2=0;i2<trChild2.length;i2++) {
				var theId = trChild2[i2].id;
				if (theId) {
					trChild2[i2].id = theId + trrows.length; //Add counter to id!!!!
					var newid = '#' + trChild2[i2].id;
				}	
				
				
				//Clear ALL the fields values
				trChild2[i2].value = '';
				
				//Adjust the HREF attributes as follows
				if (trChild2[i2].name == 'bAddDel') {	
					trChild2[i2].value = 'Remove';
					trChild2[i2].onclick = removePayment;
					trChild2[i2].style.fontSize = '8px';
				}				
			}
		}
	}
	
	//Add the new record to the document
    document.getElementById("bodyPaym").appendChild(trnew);	

    jQuery(newid).removeClass('hasDatepicker').datepicker({dateFormat: 'dd/mm/yy', changeMonth: true, changeYear: true}); 
  
	return false;
}

function AddSundry() {
	//Clone the first Item
	var trnew = document.getElementById('trSundry').cloneNode(true);

	//Now loop thru the first line of children, drill deeper for each on found
	var trChild = trnew.childNodes;
	for (var i=0;i<trChild.length;i++) {	
		if (trChild[i].nodeName == 'TD') {
			var trChild2 = trChild[i].childNodes; //Go one level deeper
			for (var i2=0;i2<trChild2.length;i2++) {
				//Clear ALL the fields values
				trChild2[i2].value = '';
				
				//Adjust the HREF attributes as follows
				if (trChild2[i2].name == 'bAddDel') {	
					trChild2[i2].value = 'Remove';
					trChild2[i2].onclick = removeSundry;
					trChild2[i2].style.fontSize = '8px';
				}				
			}
		}
	}
	
	//Add the new record to the document
    document.getElementById("bodySundry").appendChild(trnew);	

	return false;
}

function removeItem() {
	var i=this.parentNode.parentNode.rowIndex;		
	document.getElementById('tableItem').deleteRow(i);
	doTotals();
}

function removeItemAdd(varThis) {
	var i=varThis.parentNode.parentNode.rowIndex;		
	document.getElementById('tableItem').deleteRow(i);
	doTotals();
}

function removePayment() {
	var i=this.parentNode.parentNode.rowIndex;
	document.getElementById('tablePaym').deleteRow(i);
	doTotals();
}

function removePaymentAdd(varThis) {
	var i=varThis.parentNode.parentNode.rowIndex;
	document.getElementById('tablePaym').deleteRow(i);
	doTotals();
}

function removeSundry() {
	var i=this.parentNode.parentNode.rowIndex;
	document.getElementById('tableSundry').deleteRow(i);
	doTotals();
}

function removeSundryAdd(varThis) {
	var i=varThis.parentNode.parentNode.rowIndex;
	document.getElementById('tableSundry').deleteRow(i);
	doTotals();
}

function getDate() {
	var now = new Date();
    var year = now.getFullYear();
    var month = now.getMonth() + 1;
    var day = now.getDate();
//	var today = year + '-' + month + '-' + '0' + day;
	var today = year + '-' + month + '-' + day;
	return today;
}

function validate_required(field,alerttxt) {
	with (field) {
		if (value==null||value=="") {
			alert(alerttxt);
			return false;
		}
		else {
			return true;
		}
	}
}


//function validate_required(field,alerttxt,source) {
//	with (field) {
//		if (value==null||value=="") {
//			alert(alerttxt);return false;
//		}
//		else {
//			if(value!=source) {
//				document.getElementById("contract_change").value = "ContractChanged"
//			}
//			return true;
//		}
//	}
//}


//function validate_changed(field,source) {
//	with (field) {
//		if(value!=source) {
//			document.getElementById("contract_change").value = "ContractChanged"
//		}
//		return true;
//	}
//}

function validate_form_newc(thisform) {
//	alert('in');
	with (thisform)	{
//		alert('start');
		if (validate_required(ckey,"Please enter the Contract number.")==false) {
			ckey.focus();return false;
		}

		if (validate_required(date_start,"Please enter the Contract start date.")==false) {
			date_start.focus(); return false;
		}

		if (validate_required(date_end,"Please enter the Contract end date.")==false)  {
			date_end.focus();return false; 
		}

		if (validate_required(customer_name,"Please enter the Customer name.")==false)  {
			customer_name.focus();return false; 
		}

		if (validate_required(customer_address,"Please enter the Customer address.")==false)  {
			customer_address.focus();return false; 
		}

		if (validate_required(customer_cellphone,"Please enter the Customer Cellphone Number.")==false)  {
			customer_cellphone.focus();return false; 
		}

		//Only verify the Finish field if the item has been filled in
		var aa=document.getElementsByName("item");
		var aaPC=document.getElementsByName("pricecat");
		var ii=0;
		for (i=0; i<=aa.length-1;i++) {
			if (aa[i].value!=null && aa[i].value!="") {
				ii+=1;
				if (aaPC[i].value==null||aaPC[i].value=="")	{
					alert("Please select an Item Finish option");
					aaPC[i].focus();
					return false;
				}		
			}
		}
		
		//Verify if at least 1 item has been captured...
		if (ii==0) {
			alert("Please add at least one Item");
			aa[ii].focus();
			return false;
		}
		
//		var aa=document.getElementsByName("item");
//		var aaPC=document.getElementsByName("pricecat");		
//		for (i=0; i<=aa.length-1;i++) {
//			if (aa[i].value==null||aa[i].value=="")	{
//				alert("Please add Item");
//				aa[i].focus();
//				return false;
//			}
//			else {
//				if (aaPC[i].value==null||aaPC[i].value=="")	{
//					alert("Please select an Item Finish option");
//					aaPC[i].focus();
//					return false;
//				}		
//			}
//		}		

		var aa=document.getElementsByName("payment");
		var aaD=document.getElementsByName("paydatereceived");
		for (i=0; i<=aa.length-1;i++) {
			if (aa[i].value!=null && aa[i].value!="")	{
				if (aaD[i].value==null||aaD[i].value=="")	{
					alert("Please capture the Payment Date Received");
					aaD[i].focus();
					return false;
				}				
			}
		}
	}
}

//function PopDateFields(mf) {
//	var now = new Date();
//    var year = now.getFullYear();
//    var month = now.getMonth() + 1;
//    var day = now.getDate();
// 
//    if(day.length==1) {
//		var today = year + '-' + month + '-' + '0' + day;
//	}
//	else {
//		var today = year + '-' + month + '-' + day;
//	}
//
//    mf.date_start.value = today;
//    mf.paydatereceived.value = today;
//
//    year = year + 1; //Add one year for end date
//	var today = year + '-' + month + '-' + day;
//    mf.date_end.value = today;
//}

function ClearChangeField() {
    document.getElementById("contract_change").value = "";
}

function UpdateChangeField() {
	if (cc=document.getElementById("contract_change")) {
      cc.value = "ContractChanged";
	}
}

//function Lookup_dp() {
//	var a = "{{testtxt}}";
//	
////	alert(a);
//	//{% for item in items %}
//		//alert('rrr');	
//	//{% endfor %}
//}

// Client function that calls a server rpc and provides a callback
function doItemDesc(varThis) {
//	Take the id value en strip the number from the string
//	used slice, ommit the last parameter, then it copies up to the end, store it in global var
//  To be used on the callback function...
	g_counter = varThis.id.slice(4);
	
//	Fetch the Description from the Server 
	server.ItemDesc(varThis.value, onItemDescSuccess);  
}

// Callback for after a successful getDesc
function onItemDescSuccess(response) {

	var itemdesc = 'itemdesc' + g_counter;
	$(itemdesc).value = response[0];
	
	//alert(response[1]);
	var itemfinish = 'pricecat' + g_counter;
	$(itemfinish).value = response[1];	
	
	var itemfinish = 'price' + g_counter;
	$(itemfinish).value = response[2];	
	
	doTotals();
}

//Client function that calls a server rpc and provides a callback
function doItemPrice(varThis) {
//	Take the id value en strip the number from the string
//	used slice, ommit the last parameter, then it copies up to the end, store it in global var
//  To be used on the callback function...
	g_counter = varThis.id.slice(8);
	
	//Clear the pricefield
	var itemprice = 'price' + g_counter;
	$(itemprice).value = '';	
	
	var itemcode = 'item' + g_counter;
	
//	Fetch the Description from the Server 
	//alert(varThis.value);
	server.ItemPrice($(itemcode).value, varThis.value, onItemPriceSuccess);  
}

// Callback for after a successful getDesc
function onItemPriceSuccess(response) {
	var itemprice = 'price' + g_counter;
	$(itemprice).value = response;
	doTotals();	
}

function doTotals() {
	
	UpdateChangeField();
	
	var iplanfees = 0.0;
	var bb=document.getElementById("planfeesprice");
	if (!(bb.value == null || bb.value == "")) {
		iplanfees = parseFloat(bb.value).toFixed(2);
	}
	
	var itransport = 0.0;
	var bb=document.getElementById("transportprice");
	if (!(bb.value == null || bb.value == "")) {
		itransport = parseFloat(bb.value).toFixed(2);
	} 
	
	var iletter = 0.0
	var bb=document.getElementById("letterprice");
	if (!(bb.value == null || bb.value == "")) {
		iletter = parseFloat(bb.value).toFixed(2);
	}	

	var isundries = 0.0;
	var bb=document.getElementsByName("sundriesprice");
	for (i=0; i<=bb.length-1;i++) {	
		if (!(bb[i].value == null || bb[i].value == "")) {
			isundries = isundries + parseFloat(bb[i].value);
		}
	}
	
	var icontractcost = 0;
	icontractcost = parseFloat(iplanfees) + parseFloat(itransport) + parseFloat(isundries) + parseFloat(iletter);
	
	//Write the subtotal for ContractCosts
    if (bb=document.getElementById("contractcost")) {	
    	bb.value = parseFloat(icontractcost).toFixed(2);		
    }
	
					
	//Get the total for all items
	var itotitem = 0.0;
	var aa=document.getElementsByName("price");
	for (i=0; i<=aa.length-1;i++) {
		if (!(aa[i].value == null || aa[i].value == "")) {
			itotitem = itotitem + parseFloat(aa[i].value);
		}
	}	
	
	//Get the total for all additional items added
	var itotitemAdd = 0.0;
	var aaitemadd=document.getElementsByName("priceAdd");
	for (i=0; i<=aaitemadd.length-1;i++) {
		if (!(aaitemadd[i].value == null || aaitemadd[i].value == "")) {
			itotitemAdd = itotitemAdd + parseFloat(aaitemadd[i].value);
		}
	}		
	
	//Get total for all payments
	var itotpaym = 0.0;
	var aapaym=document.getElementsByName("payment");
	for (i2=0; i2<=aapaym.length-1;i2++) {
		if (!(aapaym[i2].value == null || aapaym[i2].value == "")) {		
			itotpaym = itotpaym + parseFloat(aapaym[i2].value);
		}		
	}
	
	//Get total for additional Payments Added
	var itotpaymAdd = 0.0;
	var aapaymadd=document.getElementsByName("paymentAdd");
	for (i2=0; i2<=aapaymadd.length-1;i2++) {
		if (!(aapaymadd[i2].value == null || aapaymadd[i2].value == "")) {		
			itotpaymAdd = itotpaymAdd + parseFloat(aapaymadd[i2].value);
		}		
	}
	
	//Write the total Items, right at the bottom
    if (bb=document.getElementById("TotItem")) {
    	bb.value = parseFloat(itotitem+itotitemAdd+icontractcost).toFixed(2);
    }
	//Write the subtotal for Items
    if (bb=document.getElementById("SubTotItem")) {	
    	bb.value = parseFloat(itotitem).toFixed(2);	
    }
	//Write the subtotal for AdditionalItems
    if (bb=document.getElementById("SubTotItemAdd")) {	
    	bb.value = parseFloat(itotitemAdd).toFixed(2);		
    }
	
    //-----------------------
    
	//Write the Total Payments right at the bottom
    if (bb=document.getElementById("TotPaym")) {	
    	bb.value = parseFloat(itotpaym+itotpaymAdd).toFixed(2);	
    }
	//Write the Sub total for Payments
    if (bb=document.getElementById("SubTotPaym")) {
    	bb.value = parseFloat(itotpaym).toFixed(2);	
    }
	//Write the subtotal for Additional Payments
    if (bb=document.getElementById("SubTotPaymAdd")) {	
    	bb.value = parseFloat(itotpaymAdd).toFixed(2);		
    }
    
    //-----------------------------
    
    if (bb=document.getElementById("TotDue"))	{
//    	bb.value = parseFloat((itotpaym+itotpaymAdd)-(itotitem+itotitemAdd+icontractcost)).toFixed(2);
    	bb.value = parseFloat((itotitem+itotitemAdd+icontractcost) - (itotpaym+itotpaymAdd)).toFixed(2);    	
	}
}

function doLetterCost() {
	
	var ilettercount = 0;
	var bb=document.getElementById("lettercount");
	if (!(bb.value == null || bb.value == "")) {
		ilettercount = parseInt(bb.value);
	}
	
	var ilettercost = 0.0;
	var bb=document.getElementById("lettercost");
	if (!(bb.value == null || bb.value == "")) {
		ilettercost = parseFloat(bb.value).toFixed(2);
	}	
	
	var iletterprice = parseInt(ilettercount) * parseFloat(ilettercost).toFixed(2);
	
	//Write the subtotal for ContractCosts
    if (bb=document.getElementById("letterprice")) {	
    	bb.value = parseFloat(iletterprice).toFixed(2);		
    }
	
	doTotals();	
}

function UpdateStat(varText) {
	if(varText=='Clear') {
	    document.getElementById("contract_change").value = "";
	}
	else {
		alert(document.getElementById("contract_change").value);
	}
	
}

function countL(varThis)
{
 var text1 = varThis.value;
 var text2 = text1.replace(/\s+/g , '');
 
 if (bb=document.getElementById("lettercount")) {	
 	bb.value = text2.length;		
 }
 
 doLetterCost();
}

function doCalcEnd(varThis) 
{
	debugger;
	
    var df=document.getElementById("dates").value.split('/'); // dd/mm/yyyy
    var date1=new Date(df[2], df[1]-1, df[0]);
    if (date1) 
    {
	var cp=document.getElementById("cperiod").value;	
    if (cp < 1) {
    	cp=365
    }
	date1.setDate(date1.getDate() + parseInt(cp));	
	
	var lday = parseInt(date1.getDate());
	if (lday < 10) {
	lday = '0' + lday;
    	}
    	
    	var lmonth = parseInt(date1.getMonth()+1);
    	if (lmonth < 10) {
    		lmonth = '0' + lmonth;
    	}
    	document.getElementById("datee").value = lday + '/' +
    	                                         lmonth + '/' +
    	                                         date1.getFullYear();  	                                         
    }
    
    UpdateChangeField();
}

