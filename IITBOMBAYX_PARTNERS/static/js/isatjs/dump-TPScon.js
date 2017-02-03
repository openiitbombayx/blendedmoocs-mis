
var combined_data = [['']];
var cou;
var arrStr=[];
var arrMin=[];
var nArray=[['']];
var unik;
var unikc=[['']];
var max;


function mapp(num){
			for(k=0;k<arrStr.length;k++){
				if(num==arrStr[k]) return k;
			}
		}

function remapp(num){
			for(k=0;k<arrStr.length;k++){
				if(num==k) return arrStr[k];
			}
		}



function parseCSV(icombined_data,someInt)
	{

	//*****************************Combined_Data**************************//
		cou = icombined_data[1].length; 
		//console.log(objectKeys[2]);
		function transpose(a) {
    	return Object.keys(a[0]).map(function (c) {
    	    return a.map(function (r) {
        		   return r[c];
      			  });
    		});
		}


	//++++++++++++++++++++++++++Finding unique values in an Array+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//

		function eliminateDuplicates(arr) {
  			var i,
      		len=arr.length,
     		out=[],
     		obj={};

  			for (i=0;i<len;i++) {
    			obj[arr[i]]=0;
  			}
  			for (i in obj) {
    			out.push(i);
  			}
  			return out;
		}


	var unik0=[],unik1=[],unik2=[];                              // unikc--> Contains the unique elements from all the columns as 2-D array

	if(cou==3){
		unikc[0] = (eliminateDuplicates(transpose(icombined_data)[1]));
		unikc[1] = (eliminateDuplicates(transpose(icombined_data)[2]));

		arrStr = eliminateDuplicates(unikc[0].concat(unikc[1]));
		unik = arrStr.length;
	}
	else if(cou==4){
		unikc[0] = (eliminateDuplicates(transpose(icombined_data)[1]));
		unikc[1] = (eliminateDuplicates(transpose(icombined_data)[2]));
		unikc[2] = (eliminateDuplicates(transpose(icombined_data)[3]));
		arrStr = unikc[0].concat(unikc[1]);
		arrStr= eliminateDuplicates(arrStr.concat(unikc[2])); 
		unik = arrStr.length;
	}
	else{
		arrStr = (eliminateDuplicates(transpose(icombined_data)[1]));
	}
		//unik1 = (eliminateDuplicates(transpose(icombined_data)[1]));

	//console.log(arrStr);

	max=0;
	for(i=0;i<arrStr.length;i++){
		if(arrStr[i].length>max) max= arrStr[i].length;
	}

	
		var divname= "#tabpage_2".concat(someInt);
		arrStr.sort();
		for(i=0;i<icombined_data.length;i++){
			combined_data[i]=[];
			for(j=0;j<cou;j++){
				if(j==0) combined_data[i][j]=icombined_data[i][j];
				else combined_data[i][j] = mapp(icombined_data[i][j]);	
			}
		}

		//console.log(combined_data);


// Sorting_function--> on the basis of 1st,2nd,3rd index and then by primary_key //
		Array.prototype.deepSortAlpha= function(){	

    		var itm, L=arguments.length, order=arguments;

    		var alphaSort= function(a, b){
        	//a= a.toLowerCase();
        	//b= b.toLowerCase();
        	if(a== b) return 0;
        	return a> b? 1:-1;
    		}
   			if(!L) return this.sort(alphaSort);

    		this.sort(function(a, b){
        		var tem= 0,  indx=0;
        		while(tem==0 && indx<L){
            		itm=order[indx];
            		tem= alphaSort(a[itm], b[itm]); 
            		indx+=1;        
        		}
       			return tem;
   			});
    		return this;
		}

		if(cou==3) combined_data.deepSortAlpha(1,2,0);
		else if(cou==4) combined_data.deepSortAlpha(1,2,3,0);
		else combined_data.deepSortAlpha(1,0)
		
		//console.log(combined_data);

	if(cou==3 || cou==4){
		//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++FOR 3 PHASE+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//
		var concat_data =[];
		var comb_data=[['']];

		for(i=0;i<combined_data.length;i++){
			comb_data[i]=[''];
			for(j=0;j<cou;j++){                                   //dependency
				comb_data[i][j]=combined_data[i][j+1];
			}
		}
		for(i=0;i<comb_data.length;i++){
			concat_data[i] = comb_data[i].join("");
		}
	
		//console.log(concat_data);


		//********Table of Pattern frequency--> a-->array of patterns, b-->frequency of patterns**********//
		var arr=[],brr=[], prev;

    	concat_data.sort();
    	for ( var i = 0; i < concat_data.length; i++ ) {
        	if ( concat_data[i] !== prev ) {
        		arr.push(concat_data[i]);
           		brr.push(1);
       		}else {
        		brr[brr.length-1]++;
      		}
        	prev = concat_data[i];
   		}	

   		//console.log(arr);
   		//console.log(brr);

   		//**************Re-Mapping the string array to Multidimensional array***************//

   		for(i=0;i<arr.length;i++){
   			nArray[i]=[];
   			nArray[i]=arr[i].split("");

   			for (a in nArray[i] ) {
    			nArray[i][a] = parseInt(nArray[i][a], 10); 			// Explicitly include base 
			}
				nArray[i][a]=parseInt(brr[i],10);					//frequency is stored in deepSortAlpha variable in each 1-D array
   		}
   		//console.log(nArray);
   		//console.log(nArray[0].deepSortAlpha);



   	//------------For searching in the pattern table----------------//
   		function find(key, array) {
  			// The variable results needs var in this case (without 'var' a global variable is created)
  			var results = [];
  			for (var i = 0; i < array.length; i++) {
   				if (array[i].indexOf(key) == 0) {
     				results.push(i);
    			}
  			}
  			return results;
		}

		//var srr = find(12,arr);
		//console.log(srr);


//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//
	}	
		if(cou==3){

			// document.getElementById('exp').style.display="block";
			// document.getElementById('align2').style.display="block";
			// document.getElementById('starBurst').style.display="block";
			// document.getElementById('slide').style.display="block";
			// document.getElementById('attr').style.display="block";
			// document.getElementById('voidS').style.display="block";
			// document.getElementById('restore1').style.display="block";
			// document.getElementById('ePattern').style.display="block";
		
			var s_data= cal_frq(combined_data,1);
			console.log(s_data);
			var sales_data= pass_in(s_data);


			var width = 1200, height = 510, margin ={b:0, t:40, l:170, r:50};
			// var svg = d3.select("#tabpage_2")
			var svg = d3.select(divname)
							.append("svg").attr('width',width).attr('height',(height+margin.b+margin.t))
							.append("g").attr("transform","translate("+ margin.l+","+margin.t+")");

			var data = [ 
							{data:bP.partData(sales_data,2), id:'SalesAttempts', header:["Pre-Test Score","Post-Test Score", "Control Group"]},
						];

						bP.draw2(data,svg);
		}
		else if(cou==4){

			// document.getElementById('exp').style.display="block";
			// document.getElementById('align2').style.display="block";
			// document.getElementById('starBurst').style.display="block";
			// document.getElementById('slide').style.display="block";
			// document.getElementById('attr').style.display="block";
			// document.getElementById('voidS').style.display="block";
			// document.getElementById('restore1').style.display="block";
			// document.getElementById('switch').style.display="block";
			// document.getElementById('align3').style.display="block";
			// document.getElementById('returnP').style.display="block";
			// document.getElementById('ePattern').style.display="block";

			var s_data= cal_frq(combined_data,1);
			var s_data2=cal_frq(combined_data,2);



			var sales_data= pass_in(s_data);
			var sales_data2=pass_in(s_data2);

			//var dat = [['']];

			//console.log(s);
		
			var initial_data = [['']];
			//alert(JSON.stringify(s_data, null, 4));
			var width = 1200, height = 560, margin ={b:0, t:40, l:170, r:50};
			// var svg = d3.select("#tabpage_2")
			var svg = d3.select(divname)
						.append("svg").attr('width',width).attr('height',(height+margin.b+margin.t))
						.append("g").attr("transform","translate("+ margin.l+","+margin.t+")");

			var data = [ 
						{data:bP.partData(sales_data,2), id:'SalesAttempts', header:["Q1","Q1ad", "Transition-1"]},
						{data:bP.partData(sales_data2,2), id:'SalesAttempts2', header:["","Q2", "Transition-2"]}
						];

						bP.draw2(data,svg);
		}
		else{
			var width = 1200, height = 560, margin ={b:0, t:40, l:170, r:50};
			// var svg = d3.select("#tabpage_2")
			var svg = d3.select(divname)
						.append("svg").attr('width',width).attr('height',(height+margin.b+margin.t))
						.append("g").attr("transform","translate("+ margin.l+","+margin.t+")");

			var srr=[];
			for(i=0;i<combined_data.length;i++){
				srr[i]=combined_data[i][1];
			}
			// Finding the frequency//
			var arr=[],brr=[], prev;
    		for ( var i = 0; i < srr.length; i++ ) {
        		if ( srr[i] !== prev ) {
        			arr.push(srr[i]);
           			brr.push(1);
       			}else {
        			brr[brr.length-1]++;
      			}
        		prev = srr[i];
   			}	
   			
   			bP.drawBar(arr,brr,svg);
		}
}

	function cal_frq(data,x){
		var s_data =[[0]];
		var row_max = 0;
		var col_max = 0;
		//calculate frequencies
		for(i=0; i<data.length; i++)
		{  
    		temp1 = parseInt(data[i][x]);
			//alert(temp1);
			temp2 = parseInt(data[i][x+1]);
	 
			if(!s_data[temp1])
			{
	    		s_data[temp1] = [0]
				
	  		}
			if (!s_data[temp1][temp2])
			{
	     		s_data[temp1][temp2] = new Number(0);
			}
    	s_data[temp1][temp2] += 1;
		}
					//fill zero for all places which do not have any entry//
		//*********Fill zeroes according to number of differentiating options********//


		//console.log(cou);
		for (i=0; i<unik; i++)									
		{
			//alert("row:" + sales_data.length);
   			for (j=0; j<unik; j++)
   			{
				if(!s_data[i])
				{
					s_data[i] = [0];
				}
   				if(!s_data[i][j])
   				{
					s_data[i][j] = new Number(0);
				}
   			}
		}
		console.log(s_data);
		return s_data;

		}
		
		
	function pass_in(data){
		var sales_data = [];
		for (i=0; i<data.length; i++)
			{
   			for (j=0; j<data[i].length; j++)
   				{
   					sales_data.push([parseInt(i)+'',parseInt(j)+'', parseInt(data[i][j])]); 
   				}
			}
		return sales_data;
	}

