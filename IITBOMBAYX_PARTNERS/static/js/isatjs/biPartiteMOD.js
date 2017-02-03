!function(){



	//Latest Backup-- o1
	//Secondary Backup-- o2
	//Original File-- o


	var bP={};	
	// var b=30, bb=150, height=600, buffMargin=1, minHeight=14;
	var b=30, bb=150, height=500, buffMargin=0, minHeight=14;
	var c1=[-95, 40], c2=[-50, 80], c3=[-10, 120]; //Column positions of labels.

	var colors2 =["#3366CC", "#DC3912",  "#FF9900","#109618", "#990099", "#0099C6"];
	var colors1= ["#8dd3c7","#a6cee3","#cab2d6","#6a3d9a","#b15928","#ff7f00","#a6cee3","#1f78b4","#b2df8a","#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","#cab2d6","#6a3d9a","#ffff99","#b15928"];

	var colors = ["#a6cee3","#1f78b4","#b2df8a","#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","#cab2d6","#6a3d9a","#ffff99","#b15928"];

	bP.partData = function(data,p){
		//console.log(data);
		var sData={};
		sData.keys=[
			d3.set(data.map(function(d){ return d[0];})).values(),    //.sort(function(a,b){ return ( a<b? -1 : a>b ? 1 : 0);}),
			d3.set(data.map(function(d){ return d[1];})).values()    //.sort(function(a,b){ return ( a<b? -1 : a>b ? 1 : 0);})		
		];
		//alert(d3.set(data.map(function(d){return d[0];})).values());
		//alert(d3.set(data.map(function(d){return d[1];})).values());
		//alert(sData.keys);

		
		sData.data = [	sData.keys[0].map( function(d){ return sData.keys[1].map( function(v){ return 0; }); }),
						sData.keys[1].map( function(d){ return sData.keys[0].map( function(v){ return 0; }); }) 
		];

		data.forEach(function(d){ 
			sData.data[0][sData.keys[0].indexOf(d[0])][sData.keys[1].indexOf(d[1])]=d[p];
			sData.data[1][sData.keys[1].indexOf(d[1])][sData.keys[0].indexOf(d[0])]=d[p]; 
		});
		//alert(sData.data[0]);    // --> transition 1-2 : s_Data matrix in an array, array stacked left to right, top to bottom
		//alert(sData.data[1]);    // --> transition 1-2 : s_Data matrix in an array, array stacked top to bottom, left to right
		//console.log(sData);
		return sData;
	}
	
	function visualize(data,col){
		var vis ={};
		function calculatePosition(a, s, e, b, m){
			var total=d3.sum(a);
			var sum=0, neededHeight=0, leftoverHeight= e-s-2*b*a.length;
			var ret =[];
			
			//console.log(total);
			//console.log(a);
			a.forEach(
				function(d){ 
					var v={};
					v.percent = (total == 0 ? 0 : d/total); 
					v.value=d;  
					v.height=Math.max(v.percent*(e-s-2*b*a.length), m);
					(v.height==m ? leftoverHeight-=m : neededHeight+=v.height );
					ret.push(v);
				}
			);
			
			var scaleFact=leftoverHeight/Math.max(neededHeight,1), sum=0;
			
			ret.forEach(
				function(d){ 
					d.percent = scaleFact*d.percent; 
					d.height=(d.height==m? m : d.height*scaleFact);
					d.middle=sum+b+d.height/2;
					d.y=s + d.middle - d.percent*(e-s-2*b*a.length)/2;
					d.y3=s + d.middle - d.percent*(e-s-2*b*a.length)/2 - minHeight/2;
					d.h= d.percent*(e-s-2*b*a.length);
					d.percent = (total == 0 ? 0 : d.value/total);
					sum+=2*b+d.height;
				}
			);
			//console.log(ret);
			return ret;
		}

		vis.mainBars = [ 
			calculatePosition( data.data[0].map(function(d){ return d3.sum(d);}), 0, height, buffMargin, minHeight),
			calculatePosition( data.data[1].map(function(d){ return d3.sum(d);}), 0, height, buffMargin, minHeight)
		];
		
		console.log(data.data[0].map(function(d){ return d3.sum(d);})); // ------------------------> An array of number's frequencies
		//console.log(vis.mainBars);

		vis.subBars = [[],[]];
		vis.mainBars.forEach(function(pos,p){
			pos.forEach(function(bar, i){	
				//console.log(data.data[p][i]);
				calculatePosition(data.data[p][i], bar.y, bar.y+bar.h, 0, 0).forEach(function(sBar,j){ 
					sBar.key1=(p==0 ? i : j); 
					sBar.key2=(p==0 ? j : i); 
					vis.subBars[p].push(sBar); 
				});
			});
		});
		
		vis.subBars.forEach(function(sBar){
			sBar.sort(function(a,b){ 
				return (a.key1 < b.key1 ? -1 : a.key1 > b.key1 ? 
						1 : a.key2 < b.key2 ? -1 : a.key2 > b.key2 ? 1: 0 )});
		});
		
		//console.log(vis.subBars);

	if(cou==4){
		//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//

		// Array crr contains the breakdown of subBars[0] frequency to calculate further sub-subBars
		// Array drr contains the breakdown of subBars[1] frequency to calculate further sub-subBars

		
		var temp;
		var crr=[['']],drr=[['']],q=0;
		for(i=0;i<cou;i++){
			for(j=0;j<cou;j++){
				crr[q]= srch(i,j,col);
				drr[q]=srch(j,i,col);
				q++;	
			}
		}

		function srch(i,j,s){
			var srr=[];
			for(k=0;k<cou;k++) srr[k]=0;
			if(s==0){
				for(k=0;k<nArray.length;k++){
					if(nArray[k][0]==i && nArray[k][1]==j) srr[nArray[k][2]] = nArray[k].deepSortAlpha;
				}
			}
			else{
				for(k=0;k<nArray.length;k++){
					if(nArray[k][1]==i && nArray[k][2]==j) srr[nArray[k][0]] = nArray[k].deepSortAlpha;
				}
			}
			//console.log(srr);
			return srr;

		}

		//console.log(crr);
		//console.log(drr);
		

		vis.subBars2 = [[ ],[ ]];                            //an array containing the sub-subBars

		vis.subBars.forEach(function(pos,p){
			pos.forEach(function(bar, i){
				if(p==0){
					//console.log(crr[i]);
					calculatePosition(crr[i], bar.y, bar.y+bar.h, 0, 0).forEach(function(sBar,j){ 
						sBar.key1=bar.key1 ; 
						sBar.key2= bar.key2 ;
						sBar.key3=j; 
						//console.log(sBar);
						vis.subBars2[0].push(sBar); 
					});
				}
				else{
					calculatePosition(crr[i], bar.y, bar.y+bar.h, 0, 0).forEach(function(sBar,j){ 
						sBar.key1=bar.key1 ; 
						sBar.key2= bar.key2 ;
						sBar.key3=j; 
						vis.subBars2[1].push(sBar); 
					});
				}	
				
			});
		});

		vis.subBars2.forEach(function(sBar){
			sBar.sort(function(a,b){ 
				return (a.key1 < b.key1 ? -1 : a.key1 > b.key1 ? 
						1 : a.key2 < b.key2 ? -1 : a.key2 > b.key2 ? 1: a.key3 < b.key3 ? -1 : a.key3 > b.key3 ? 1:0)});
		});

		//console.log(vis.subBars2);

		vis.edges2 = vis.subBars2[0].map(function(p,i){
			return {
				key1: p.key1,
				key2: p.key2,
				key3: p.key3,
				y1:p.y,
				y2:vis.subBars2[1][i].y,
				h1:p.h,
				h2:vis.subBars2[1][i].h
			};
		});

		//console.log(vis.edges2);
	//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//
	}
	
	
		vis.edges = vis.subBars[0].map(function(p,i){
			return {
				key1: p.key1,
				key2: p.key2,
				y1:p.y,
				y2:vis.subBars[1][i].y,
				h1:p.h,
				h2:vis.subBars[1][i].h
				
			};
		});
		vis.keys=data.keys;

		//console.log(vis.edges);

		//console.log(vis.subBars[0][9]);    //--> Transition 1-4 for both the data set in p=0
		//console.log(vis.subBars[1][9]);    //--> Transition 1-4 for both the data set in p=1
		return vis;

	}
	
	function arcTween(a) {
		var i = d3.interpolate(this._current, a);
		this._current = i(0);
		return function(t) {
			return edgePolygon(i(t));
		};
	}
	
	function drawPart(data, id, p,s){

		if(p==0){
			c1[p] -= 5*max;
			
		} 
		else{
			c1[p] += 2*max;
			c2[p] += 6*max;
			c3[p] += 6*max;
			
		}
		if(id=="Last" && cou==3) d3.select("#"+id).append("g").attr("class","part"+p)
			.attr("transform","translate("+ p*(b+60) +",0)"); 
		else	
		d3.select("#"+id).append("g").attr("class","part"+p)
			.attr("transform","translate("+ p*(bb+b) +",0)");  //---->
		d3.select("#"+id).select(".part"+p).append("g").attr("class","subbars");
		d3.select("#"+id).select(".part"+p).append("g").attr("class","subbars2");                   //****NewAddition****//
		d3.select("#"+id).select(".part"+p).append("g").attr("class","mainbars");
		d3.select("#"+id).select(".part"+p).append("g").attr("class","path");
		
		var mainbar = d3.select("#"+id).select(".part"+p).select(".mainbars")
			.selectAll(".mainbar").data(data.mainBars[p])
			.enter().append("g").attr("class","mainbar");


		mainbar.append("rect").attr("class","mainrect")
			.attr("x", 0).attr("y",function(d){ return d.middle-d.height/2; })
			.attr("width",b).attr("height",function(d){ return d.height; })                       // b--> width of the bar
			.style("shape-rendering","auto")
			.style("fill-opacity",0).style("stroke-width","0.5")
			.style("stroke","black").style("stroke-opacity",0);

		
		//**************Adding the text elements*****************************//
		if((p || (s==0)) && id!='Last'){			

			mainbar.append("text").attr("class","barlabel")
			.attr("x", c1[p]).attr("y",function(d){ return d.middle+5;})
			.text(function(d,i){return remapp(data.keys[p][i]); })
			.attr("text-anchor","start" );
			
//return (parseInt(data.keys[p][i])+parseInt(arrMin[p+s+1]));

			mainbar.append("text").attr("class","barvalue")
			.attr("x", c2[p]).attr("y",function(d){ return d.middle+5;})
			.text(function(d,i){ return d.value ;})
			.attr("text-anchor","end");
			
			mainbar.append("text").attr("class","barpercent")
			.attr("x", c3[p]).attr("y",function(d){ return d.middle+5;})
			.text(function(d,i){ return Math.round(100*d.percent)+"%" ;})
			.attr("text-anchor","end").style("fill","grey");

			//+++++++++++++++++++++++++++++++++++++++++++++++++++++++//
			var sum1=0;
			for(i=0;i<data.mainBars[p].length;i++){
				sum1 += data.mainBars[p][i].value;
			}
			//console.log(data);
			mainbar.append("text").attr("class","labelvalue1")
			.attr("x", c2[p]).attr("y",height+30)
			.text( sum1 )
			.attr("text-anchor","end");

			//+++++++++++++++++++++++++++++++++++++++++++++++++++++//

			if((p==0 && s==0) || (p==1 && s==1)){
				var sum2=0;
			for(i=0;i<data.edges.length;i++){
				//var sty= d3.select("#"+id).select(".edges").selectAll(".edge").filter(function(d){ return d== data.edges[i];}).style("opacity");
				if(data.edges[i].h1 !=0 && data.edges[i].h2 !=0){
					if(p==0) sum2 += data.subBars[1-p][i].value;
					else
						sum2 += data.subBars[p][i].value;					
				}
			}
			console.log(data.edges);	
			//console.log(sum2); 

			mainbar.append("text").attr("class","labelvalue2")
			.attr("x", -c2[p]).attr("y",height+30)
			.text( sum2 )
			.attr("text-anchor","end");
			}

			

			
		}


		//*********************Appending the separating lines***********************//
		if(id=='Last' || p==0){

			mainbar.append("rect").attr("class","path1")
			.attr("x", -100-5*max).attr("y",function(d){ 
				if(d.value ==0) return (d.y-7);
				return d.y; }) 								 //-----Line oriented towards the left side
			.attr("width",(b+100+5*max)).attr("height",1)                       
			.attr("stroke","grey");	

				//*****Creating the last line****//
			mainbar.append("rect").attr("class","path1")
			.attr("x", -100-5*max).attr("y",height)
			.attr("width",(b+100+5*max)).attr("height",1)                       
			.attr("stroke","grey");
		}

		else{
			mainbar.append("rect").attr("class","path1")
			.attr("x", 0).attr("y",function(d){ 
				if(d.value ==0) return (d.y-7);
				return d.y; })   							 //-----Line oriented towards the right side
			.attr("width",(b+100+5*max)).attr("height",1)                       
			.attr("stroke","grey");
				//*****Creating the last line****//
			mainbar.append("rect").attr("class","path1")
			.attr("x", 0).attr("y",height)
			.attr("width",(b+100+5*max)).attr("height",1)                       // b--> width of the bar
			.attr("stroke","grey");
		}

		//***********************Appending the enclosing rectangle********************//
		if(p==0 && s==0){
			mainbar.append("rect").attr("class","path1")
			.attr("x", -100-5*max).attr("y",function(d){ return d.middle-d.height/2; })
			.attr("width",0.5).attr("height",function(d){ return d.height; })                       
			.attr("stroke","grey");	

			mainbar.append("text").attr("class","label")
			.attr("x", c1[p]).attr("y",height+30)
			.text("N")
			.attr("text-anchor","start").style("fill","grey");
		}


		//************************* Creating Subbars for the 'Last' bar*****************//
		if(id=='Last'){
			d3.select("#"+id).select(".part"+p).select(".subbars")
				.selectAll(".subbar").data(data.subBars[p]).enter()
				.append("rect").attr("class","subbar")
				.attr("x", 0).attr("y",function(d){ return d.y})
				.attr("width",b).attr("height",function(d){ return d.h})
				.style("fill",function(d){ return colors[d.key2];});

		if(cou==4){
			d3.select("#"+id).select(".part"+p).select(".subbars2")
				.selectAll(".subbar2").data(data.subBars2[p]).enter()
				.append("rect").attr("class","subbar2")
				.attr("x", 0).attr("y",function(d){ return d.y})
				.attr("width",b).attr("height",function(d){ return d.h})
				.style("fill",function(d){ return colors[d.key2];});
			}

			
		}

		else{
			d3.select("#"+id).select(".part"+p).select(".subbars")
				.selectAll(".subbar").data(data.subBars[p]).enter()
				.append("rect").attr("class","subbar")
				.attr("x", 0).attr("y",function(d){ return d.y})
				.attr("width",b).attr("height",function(d){ return d.h})
				.style("fill",function(d){ return colors[d.key1];});

		if(cou==4){
			d3.select("#"+id).select(".part"+p).select(".subbars2")
				.selectAll(".subbar2").data(data.subBars2[p]).enter()
				.append("rect").attr("class","subbar2")
				.attr("x", 0).attr("y",function(d){ return d.y})
				.attr("width",b).attr("height",function(d){ return d.h})
				.style("fill",function(d){ return colors[d.key1];});
			}	
		}
		
	}


	
	function drawEdges(data, id,s){

		if(cou==4){
			//****************sub-subBars Edges*************************//

			d3.select("#"+id).append("g").attr("class","edges2").attr("transform","translate("+ b +",0)");

			d3.select("#"+id).select(".edges2").selectAll(".edge2")
				.data(data.edges2).enter().append("polygon").attr("class","edge2")
				.attr("points", edgePolygon).style("fill",function(d){ return colors[d.key1];})
				.style("opacity",0.5).each(function(d) { this._current = d; });	
		}
		

		//****************subBars Edges*************************//

		d3.select("#"+id).append("g").attr("class","edges").attr("transform","translate("+ b +",0)");

		d3.select("#"+id).select(".edges").selectAll(".edge")
			.data(data.edges).enter().append("polygon").attr("class","edge")
			.attr("points", edgePolygon).style("fill",function(d){ return colors[d.key1];})
			.style("opacity",0.5).each(function(d) { this._current = d; });	


		

			// Define the div for the tooltip
			var div = d3.select("body").append("div")	
    		.attr("class", "tooltip")				
    		.style("opacity", 0);

		d3.select("#"+id).select(".edges").selectAll(".edge")
			.filter(function(d){
					return (d.h1 !=0 && d.h2 !=0);
				})
			.on("mouseover", function(d) {		
            	div.transition()		
                	.duration(200)		
                	.style("opacity", .9);
                //alert(data.subBars[s][unik*d.key1+d.key2].value);		
            	div	.html(data.subBars[s][unik*d.key1+d.key2].value + "<br/>")	
                	.style("left", (d3.event.pageX) + "px")		
                	.style("top", (d3.event.pageY) + "px");	
            	})					
        	.on("mouseout", function(d) {		
           		div.transition()		
                	.duration(500)		
                	.style("opacity", 0);	
                	//.style('pointer-events', 'none')
                	});  
	}	
	
	function drawHeader(header, id){
		
		d3.select("#"+id).append("g").attr("class","header").append("text").text(header[2])
			.style("font-size","14").attr("x",108).attr("y",-20).style("text-anchor","middle")
			.style("font-weight","bold");
		
		[0,1,2].forEach(function(d){
			var h = d3.select("#"+id).select(".part"+d).append("g").attr("class","header");
			
			h.append("text").text(header[d]).attr("x", (c1[d]-5))
				.attr("y", -5).style("fill","grey");
			
			//h.append("text").text("Count").attr("x", (c2[d]+10))
			//	.attr("y", -5).style("fill","grey");
			
			//h.append("line").attr("x1",c1[d]-10).attr("y1", -2)
			//	.attr("x2",c3[d]+10).attr("y2", -2).style("stroke","black")
			//	.style("stroke-width","1").style("shape-rendering","crispEdges");
		});
	}
	
	function edgePolygon(d){
		return [0, d.y1, bb, d.y2, bb, d.y2+d.h2, 0, d.y1+d.h1].join(" ");
	}	
	
	function transitionPart(data, id, p){
		var mainbar = d3.select("#"+id).select(".part"+p).select(".mainbars")
			.selectAll(".mainbar").data(data.mainBars[p]);
		
		mainbar.select(".mainrect").transition().duration(500)
			.attr("y",function(d){ return d.middle-d.height/2;})
			.attr("height",function(d){ return d.height;});
			
		mainbar.select(".barlabel").transition().duration(500)
			.attr("y",function(d){ return d.middle+5;});
			
		mainbar.select(".barvalue").transition().duration(500)
			.attr("y",function(d){ return d.middle+5;}).text(function(d,i){ return d.value ;});
			
		mainbar.select(".barpercent").transition().duration(500)
			.attr("y",function(d){ return d.middle+5;})
			.text(function(d,i){ return Math.round(100*d.percent)+"%" ;});

		var sum1=0;
			for(i=0;i<data.mainBars[p].length;i++){
				sum1 += data.mainBars[p][i].value;
			}
			//console.log(data);
	
		mainbar.select(".labelvalue1").transition().duration(500)
			.text( sum1 );

		//console.log(data.edges); 

		
		var sum2=0;
		for(i=0;i<data.edges.length;i++){
				if(data.edges[i].h1 !=0 && data.edges[i].h2 !=0){
					if(p==0) sum2 += data.subBars[p][i].value;
					else
						sum2 += data.subBars[p][i].value;					
				}
			

		mainbar.select(".labelvalue2").transition().duration(500)
			.text( sum2 );
		}

					
		d3.select("#"+id).select(".part"+p).select(".subbars")
			.selectAll(".subbar").data(data.subBars[p])
			.transition().duration(500)
			.attr("y",function(d){ return d.y}).attr("height",function(d){ return d.h});

		
		if(cou==4){
			d3.select("#"+id).select(".part"+p).select(".subbars2")
				.selectAll(".subbar2").data(data.subBars2[p])
				.transition().duration(500)
				.attr("y",function(d){ return d.y}).attr("height",function(d){ return d.h});
		}

		mainbar.select(".path1").transition().duration(500)
			.attr("y",function(d){ 
				if(d.value ==0) return (d.y-7);
				return d.y;})
			.attr("height",1);

	}
	
	function transitionEdges(data, id,s){

		if(cou==4){
			//********sub-subBars edges transition********//

			d3.select("#"+id).append("g").attr("class","edges2")
				.attr("transform","translate("+ b+",0)");

			d3.select("#"+id).select(".edges2").selectAll(".edge2").data(data.edges2)
				.transition().duration(500)
				.attrTween("points", arcTween)
				.style("opacity",function(d){ return (d.h1 ==0 || d.h2 == 0 ? 0 : 0.5);});

		}

		
		//********subBars edges transition********//
		d3.select("#"+id).append("g").attr("class","edges")
			.attr("transform","translate("+ b+",0)");

		d3.select("#"+id).select(".edges").selectAll(".edge").data(data.edges)
			.transition().duration(500)
			.attrTween("points", arcTween)
			.style("opacity",function(d){ return (d.h1 ==0 || d.h2 == 0 ? 0 : 0.5);});	

		//console.log(data.subBars);

			

		// Define the div for the tooltip
			//var div = d3.select("body").append("div")	
    		//.attr("class", "tooltip")				
    		//.style("opacity", 0);
/*
		d3.select("#"+id).select(".edges").selectAll(".edge").data(data.edges)
			.on("mouseover", function(d) {		
            	div.transition()		
                	.duration(200)		
                	.style("opacity", .9);		
            	div.html((data.subBars[s][unik*d.key1+d.key2]).value + "<br/>")	
                	.style("left", (d3.event.pageX) + "px")		
                	.style("top", (d3.event.pageY) + "px");	
            	})					
        	.on("mouseout", function(d) {		
           		div.transition()		
                	.duration(500)		
                	.style("opacity", 0);	
                	//.style('pointer-events', 'none')
                	});
*/			
        	//console.log(data.subBars[s]);
				
/*
        	d3.select("#"+k.id).select(".edges").selectAll(".edge")
				.filter(function(d){
					var loc= 5*d.key1 + d.key2;
					for(i=0;i<initial_data.length;i++){
						if(loc == initial_data[i]) return true;
					}
				})
				.style("fill","black");
*/              
	}
	
	function transition(data, id,s){
		if(id=='Last') transitionPart(data,id,1);
		else{
			transitionPart(data, id, 0);
			transitionPart(data, id, 1);
			transitionEdges(data, id,s);
		}
	}


bP.drawBar= function(arr,brr,svg){
	svg.append("g")
				.attr("class", "chart")
				.attr("transform","translate("+ (0)+",0)");

	var initial=[['']],k=0;
			for(i=0;i<arr.length;i++){
						initial[i]=[];
						initial[i][0]=arr[i];
						initial[i][1]=brr[i]; 
			}

	var width = 500,
		width1=350,
    	barHeight = (height/arr.length)/2;

	var x = d3.scale.linear()
   		.domain([0, d3.max(transpose(initial)[1])])
    	.range([0, width1]);

	var chart = d3.select(".chart")
    	.attr("width", width)
    	.attr("height", barHeight * (transpose(initial)[1]).length)
    	.attr("opacity",0.9);
    
	var bar = chart.selectAll("g")
    	.data(initial)
  		.enter().append("g")
    	.attr("transform", function(d, i) { return "translate(" + 250 + "," + i * barHeight + ")"; });

	bar.append("text")
		.attr("x",function(d) { return (0- (width1/2)); })
		.attr("y",barHeight/2)
		.attr("dy", ".35em")
    	.text(function(d,i) { return remapp((transpose(initial))[0][i]); });

	bar.append("rect")
	    .attr("width", function(d,i) { return x((transpose(initial))[1][i]); })
    	.attr("height", barHeight - 10);

	bar.append("text")
    	.attr("x", function(d,i) { return x((transpose(initial))[1][i]) - (.025*x((transpose(initial))[1][i])); })
    	.attr("y", barHeight / 2)
    	.attr("dy", ".35em")
    	.text(function(d,i) { return ((transpose(initial))[1][i]); });

} 

bP.draw2 = function(data,svg){
		var m=0;
		data.forEach(function(biP,s){
			if(svg=="svg2")  var d= 580;
			else var d=0;
			svg.append("g")
				.attr("id", biP.id)
				.attr("transform","translate("+ (310*s+11*max*s)+","+d+")");
			//console.log(combined_data);
			//console.log(s);
			//console.log(biP.id);
			//console.log(cou);

	//-----------------------------------Drawing the Bars and Edges for the Graph-----------------------------------//
			var visData = visualize(biP.data,s);                          
			drawPart(visData, biP.id, 0,s);
			drawPart(visData, biP.id, 1,s);
			drawEdges(visData, biP.id,s);
			drawHeader(biP.header, biP.id);


			// For drawing the 5th bar
			if(s>0 || cou==3){
				svg.append("g")										
					.attr("id", 'Last')
					.attr("transform","translate("+ ((220*(s+1))+11*max*(s+1))+","+d+")");
				drawPart(visData, 'Last', 1,s);
			}
				
	//--------------------------------------------------------------------------------------------------------------//
	//---------------------------Defining the interactivity for edges and tooltip-----------------------------------//

			// Define the div for the tooltip
			

    		if(cou>3){
    			d3.select("#"+biP.id).select(".edges").selectAll(".edge")
				.on("click",function(d,i){
					//d3.select(this).style("fill", "black");
				return plot(data,d,i,s);});
			/*	
			.on("mouseover", function(d) {		
            	div.transition()		
                	.duration(200)		
                	.style("opacity", .9);		
            	div	.html(visData.subBars[s][unik*d.key1+d.key2].value + "<br/>")	
                	.style("left", (d3.event.pageX) + "px")		
                	.style("top", (d3.event.pageY) + "px");	
            	})					
        	.on("mouseout", function(d) {		
           		div.transition()		
                	.duration(500)		
                	.style("opacity", 0);	
                	//.style('pointer-events', 'none')
                	});
             */	
            //	.on("mouseout",function(d,i){                        //****Retrieving original color on Mouseout****//
			//	d3.select(this).style("fill", colors[d.key1]);
			//	});
    		}
			


	//--------------------------------------------Defining the interactivity for Bars---------------------------//
	
			[s].forEach(function(p){	                                  	
				d3.select("#"+biP.id)
					.select(".part"+s)
					.select(".mainbars") 
					.selectAll(".mainbar")
					.on("click",function(d, i){ return bP.selectSegment(data,s,i,s); })
					//.on("mouseout",function(d, i){ return bP.deSelectSegment(data, s, i); });	
			});

			var d;
			if(cou==3)d=1;
			else d=1;

			[d].forEach(function(p){	                                  	
				d3.select("#"+"Last")
					.select(".part"+d)
					.select(".mainbars") 
					.selectAll(".mainbar")
					.on("click",function(d, i){ return bP.selectSegment(data,1,i,d); })
					//.on("mouseout",function(d, i){ return bP.deSelectSegment(data, s, i); });	
			});


			[1-s].forEach(function(p){			
				d3.select("#"+biP.id)
					.select(".part"+(1-s))
					.select(".mainbars")
					.selectAll(".mainbar")
					.on("click",function(d, i){ return bP.selectSegment(data, 1-s, i,s); })
					//.on("mouseout",function(d, i){ return bP.deSelectSegment(data, 1-s, i); });	
			});

			
	//----------------------------------------------------------------------------------------------------------//
	//----------------------------------Patterns and HTML Elements----------------------------------------------//
	
			document.getElementById("restore1").onclick = function() {
			 	restore(data);
				return bP.deSelectSegment(data, s, i);
			};
			//document.getElementById("restore2").onclick = function() { restore(data)};
			if(document.getElementById('align3').style.display !="block")document.getElementById("align3").onclick = function() { align33(data)};    			
			
			if(document.getElementById('align2').style.display !="block") document.getElementById("align2").onclick = function() { alignBy(data)};
			if(document.getElementById('starBurst').style.display !="block") document.getElementById("starBurst").onclick = function() { star(data,0)};
			if(document.getElementById('slide').style.display !="block") document.getElementById("slide").onclick = function() { slid(data,0)};
			if(document.getElementById('attr').style.display !="block") document.getElementById("attr").onclick = function() { clickAttr(data,1,s)};       //Setting p=1 since transition would occur to second bar only
			if(document.getElementById('voidS').style.display !="block") document.getElementById("voidS").onclick = function() { voidS(data)};
			if(document.getElementById('switch').style.display !="block") document.getElementById("switch").onclick = function() { switchF(data,svg);};
			if(document.getElementById('ePattern').style.display !="block") document.getElementById("ePattern").onclick = function() { enterP(data)}; 
			if(document.getElementById('returnP').style.display !="block") document.getElementById("returnP").onclick = function() { returnP(data)};
			  
			

	//----------------------------------------------------------------------------------------------------------//

		});			
	}


	//****************************************************************************************************//

	function transpose(a) {
    	return Object.keys(a[0]).map(function (c) {
    	    return a.map(function (r) {
        		   return r[c];
      			  });
    		});
		}


	function plot(data,d,n,q){
		if(q==0) return plot1(data,d,n);
		else return plot2(data,d,n);

}

	function plot1(data,d,n){
		var newdata =  {keys:[], data:[]};
		data.forEach(function(k,x){
			//var a = x;
			//console.log(k.data.data[m]);
			newdata.keys = k.data.keys.map( function(d){ return d;});

			if(x==0)
			{
				var initial_data = [['']];
				for (i=0,j=0; i<combined_data.length; i++)
					{
						
   						temp1 = parseInt(combined_data[i][1]);
   						if(temp1 != d.key1)continue;
   						initial_data[j]=[];
   						initial_data[j][0] = parseInt(combined_data[i][0]);
   						initial_data[j][1] = parseInt(combined_data[i][1]);
   						initial_data[j][2] = parseInt(combined_data[i][2]);
   						j++;

					}

				var s_data3 = cal_frq(initial_data,1);
				//console.log(s_data3);
				newdata.data[0] = s_data3.map( function(d){ return d;});
				//newdata.data[0]	= transpose(s_data3);


				var initial_data = [['']];
				for (i=0,j=0; i<combined_data.length; i++)
					{
			
   						temp = parseInt(combined_data[i][2]);
   						if(temp != d.key2)continue;
   						initial_data[j]=[];
   						initial_data[j][0] = parseInt(combined_data[i][0]);
   						initial_data[j][1] = parseInt(combined_data[i][1]);
   						initial_data[j][2] = parseInt(combined_data[i][2]);
   						j++;

					}

				var s_data3 = cal_frq(initial_data,1);
				//console.log(s_data3);
				newdata.data[1] = transpose(s_data3);
				//newdata.data[1] = s_data3.map( function(d){ return d;});

			}
			else
			{	
					var initial_data2 = [['']];
					for (i=0,j=0; i<combined_data.length; i++)
							{
								//temp1 = parseInt(combined_data[i][1]);
   								temp2 = parseInt(combined_data[i][2]);
   								if(temp2 != d.key2)continue;
   								initial_data2[j]=[];
   								initial_data2[j][0] = parseInt(combined_data[i][0]);
   								initial_data2[j][1] = parseInt(combined_data[i][1]);
   								initial_data2[j][2] = parseInt(combined_data[i][2]);
   								j++;

							}

					var s_data3 = cal_frq(initial_data2,1);
					//console.log(s_data3);
					//newdata.data[0] = s_data3.map( function(d){ return d;});
					newdata.data[0] = transpose(s_data3);
					//console.log(newdata.data[0]);

					var initial_data = [['']];
					for (i=0,j=0; i<combined_data.length; i++)
					{
			
   						temp1 = parseInt(combined_data[i][1]);
   						temp2 = parseInt(combined_data[i][2]);
   						if(temp1 != d.key1 || temp2 != d.key2)continue;
   						initial_data[j]=[];
   						initial_data[j][0] = parseInt(combined_data[i][0]);
   						initial_data[j][1] = parseInt(combined_data[i][2]);
   						initial_data[j][2] = parseInt(combined_data[i][3]);
   						j++;

					}

					var s_data3 = cal_frq(initial_data,1);	
					//console.log(s_data3);

					//newdata.data[1] = s_data3.map( function(d){ return d;});
					newdata.data[1] = transpose(s_data3);
					//console.log(newdata.data[0]);		
					//console.log(newdata.data[1]);
					//console.log(newdata.data[1-m]);
			}
			transition(visualize(newdata), k.id,x);
			transition(visualize(newdata),'Last',x);
			});
			
	
	}

function plot2(data,d,n){
		var newdata =  {keys:[], data:[]};
		data.forEach(function(k,x){

			var a=x;
			//console.log(k.data.data[m]);
			newdata.keys = k.data.keys.map( function(d){ return d;});
			if(x)
			{
				var initial_data2 = [['']];
				for (i=0,j=0; i<combined_data.length; i++)
					{
			
   						temp2 = parseInt(combined_data[i][2]);
   						if(temp2 != d.key1)continue;
   						initial_data2[j]=[];
   						initial_data2[j][0] = parseInt(combined_data[i][0]);
   						initial_data2[j][1] = parseInt(combined_data[i][2]);
   						initial_data2[j][2] = parseInt(combined_data[i][3]);
   						j++;

					}

				var s_data3 = cal_frq(initial_data2,1);
				//console.log(s_data3);
				newdata.data[0] = s_data3.map( function(d){ return d;});
				//newdata.data[1] = transpose(s_data3);

				var initial_data = [['']];
				for (i=0,j=0; i<combined_data.length; i++)
					{
			
   						temp1 = parseInt(combined_data[i][3]);
   						if(temp1 != d.key2)continue;
   						initial_data[j]=[];
   						initial_data[j][0] = parseInt(combined_data[i][0]);
   						initial_data[j][1] = parseInt(combined_data[i][2]);
   						initial_data[j][2] = parseInt(combined_data[i][3]);
   						j++;

					}

				var s_data3 = cal_frq(initial_data,1);
				//console.log(s_data3);
				newdata.data[1] = transpose(s_data3);	

			}
			else
			{	
					var initial_data = [['']];

					for (i=0,j=0; i<combined_data.length; i++)
					{
			
   						temp1 = parseInt(combined_data[i][2]);
   						temp2 = parseInt(combined_data[i][3]);
   						if(temp1 != d.key1 || temp2 != d.key2)continue;
   						initial_data[j]=[];
   						initial_data[j][0] = parseInt(combined_data[i][0]);
   						initial_data[j][1] = parseInt(combined_data[i][1]);
   						initial_data[j][2] = parseInt(combined_data[i][2]);
   						j++;

					}

					var s_data3 = cal_frq(initial_data,1);	
					newdata.data[0] = s_data3.map( function(d){ return d;});
					//console.log(newdata.data[1-m]);

					var initial_data2 = [['']];
					for (i=0,j=0; i<combined_data.length; i++)
						{
			
   							temp2 = parseInt(combined_data[i][2]);
   							if(temp2 != d.key1)continue;
	   						initial_data2[j]=[];
   							initial_data2[j][0] = parseInt(combined_data[i][0]);
   							initial_data2[j][1] = parseInt(combined_data[i][1]);
   							initial_data2[j][2] = parseInt(combined_data[i][2]);
   							j++;

						}

					var s_data3 = cal_frq(initial_data2,1);
					//console.log(s_data3);
					newdata.data[1] = transpose(s_data3);//.map( function(d){ return d;});

					
			}

			transition(visualize(newdata), k.id,x);
			transition(visualize(newdata),'Last',x);
		});

			
	
	}


bP.selectSegment = function(data, m, s,s1){

	if(m==0 && s1==0){
		var newdata =  {keys:[], data:[]};
		data.forEach(function(k,x){
			
			//console.log(k.data.data[m]);
			newdata.keys = k.data.keys.map( function(d){ return d;});

			if(!x)
			{
				newdata.data[m] = k.data.data[m].map( function(d){ return d;});			
				newdata.data[1-m] = k.data.data[1-m]
					.map( function(v){ return v.map(function(d, i){ return (s==i ? d : 0);}); });
				//console.log(newdata.data[1-m]);
			}
			else
			{	
					var initial_data = [['']];

					for (i=0,j=0; i<combined_data.length; i++)
					{
   						temp1 = parseInt(combined_data[i][1]);
   						if(temp1 != s)continue;
   						initial_data[j]=[];
   						initial_data[j][0] = parseInt(combined_data[i][0]);
   						initial_data[j][1] = parseInt(combined_data[i][2]);
   						initial_data[j][2] = parseInt(combined_data[i][3]);
   						j++;

					}

					var s_data3 = cal_frq(initial_data,1);
					//console.log(s_data3);
					newdata.data[m] = s_data3.map( function(d){ return d;});	
					//console.log(newdata.data[m]);		
					newdata.data[1-m] = transpose(s_data3);
					//console.log(newdata.data[1-m]);
			}

			transition(visualize(newdata), k.id,s);
			//console.log(visualize(newdata));

			var selectedBar = d3.select("#"+k.id).select(".part"+m).select(".mainbars")
				.selectAll(".mainbar").filter(function(d,i){ return (i==s);});
			
			selectedBar.select(".mainrect").style("stroke-opacity",1);			
			selectedBar.select(".barlabel").style('font-weight','bold');
			selectedBar.select(".barvalue").style('font-weight','bold');
			selectedBar.select(".barpercent").style('font-weight','bold');
			//m=1-m;

		});
			transition(visualize(newdata), 'Last',s);

		}

	else if(m==1 && s1==1){
		var newdata =  {keys:[], data:[]};
		data.forEach(function(k,x){
			
			//console.log(k.data.data[m]);
			newdata.keys = k.data.keys.map( function(d){ return d;});
			if(x)
			{
				newdata.data[m] = k.data.data[m].map( function(d){ return d;});			
				newdata.data[1-m] = k.data.data[1-m]
					.map( function(v){ return v.map(function(d, i){ return (s==i ? d : 0);}); });
				//console.log(newdata.data[1-m]);
			}
			else
			{	
					var initial_data = [['']];

					for (i=0,j=0; i<combined_data.length; i++)
					{
			
   						temp1 = parseInt(combined_data[i][3]);
   						if(temp1 != s)continue;
   						initial_data[j]=[];
   						initial_data[j][0] = parseInt(combined_data[i][0]);
   						initial_data[j][1] = parseInt(combined_data[i][1]);
   						initial_data[j][2] = parseInt(combined_data[i][2]);
   						j++;

					}

					var s_data3 = cal_frq(initial_data,1);
					//console.log(s_data3);
					newdata.data[1-m] = s_data3.map( function(d){ return d;});	
					//console.log(newdata.data[m]);		
					newdata.data[m] = transpose(s_data3);
					//console.log(newdata.data[1-m]);
					
			}

			transition(visualize(newdata), k.id,s);
			//console.log(visualize(newdata));

			var selectedBar = d3.select("#"+k.id).select(".part"+m).select(".mainbars")
				.selectAll(".mainbar").filter(function(d,i){ return (i==s);});
			
			selectedBar.select(".mainrect").style("stroke-opacity",1);			
			selectedBar.select(".barlabel").style('font-weight','bold');
			selectedBar.select(".barvalue").style('font-weight','bold');
			selectedBar.select(".barpercent").style('font-weight','bold');
			//m=1-m;

		});
			transition(visualize(newdata), 'Last',s);

	}

	else{
		if(m==0 && s1==1) m=1-m;
		var newdata =  {keys:[], data:[]};	
		data.forEach(function(k){
			
				
			newdata.keys = k.data.keys.map( function(d){ return d;});

			//console.log(newdata.keys);			
			newdata.data[m] = k.data.data[m].map( function(d){ return d;});

			//console.log(newdata.data[m]);
			
			newdata.data[1-m] = k.data.data[1-m]
				.map( function(v){ return v.map(function(d, i){ return (s==i ? d : 0);}); });
			
			//console.log(newdata.data[1-m]);

			transition(visualize(newdata), k.id,s);
			//console.log(visualize(newdata));
				
			var selectedBar = d3.select("#"+k.id).select(".part"+m).select(".mainbars")
				.selectAll(".mainbar").filter(function(d,i){ return (i==s);});
			
			selectedBar.select(".mainrect").style("stroke-opacity",1);			
			selectedBar.select(".barlabel").style('font-weight','bold');
			selectedBar.select(".barvalue").style('font-weight','bold');
			selectedBar.select(".barpercent").style('font-weight','bold');

			if(m==1 && s1==0) m=0;
			if(m==1 && s1==1) m=1-m;
		});
			transition(visualize(newdata), 'Last',s);

		}

		
	}	
	
	bP.deSelectSegment = function(data, m, s){
		data.forEach(function(k){
			transition(visualize(k.data), k.id);
			
			var selectedBar = d3.select("#"+k.id).select(".part"+m).select(".mainbars")
				.selectAll(".mainbar").filter(function(d,i){ return (i==s);});
			
			selectedBar.select(".mainrect").style("stroke-opacity",0);			
			selectedBar.select(".barlabel").style('font-weight','normal');
			selectedBar.select(".barvalue").style('font-weight','normal');
			selectedBar.select(".barpercent").style('font-weight','normal');
		});
		if(cou==3)
			transition(visualize(data[0].data), 'Last',s);
		else transition(visualize(data[1].data), 'Last',s);
	}
	
	this.bP = bP;



	//********************************************PATTERNS******************************************//
							//*****************Onto same diagram******************//

	function clickAttr(data,p,s){
		var val = prompt("Enter the criteria value");
		star(data,mapp(val));
	}

	function enterP(data){
		var p1 = prompt("Enter the 1st value");
		var p2 = prompt("Enter the 2nd value");
		if(cou==4){
			var p3 = prompt("Enter the 3rd value");
			p3 = mapp(p3);
		} 

		p1 = mapp(p1);
		p2 = mapp(p2);
		
		data.forEach(function(biP,s){
			d3.select("#"+biP.id).select(".edges").selectAll(".edge")
			.style("opacity",0);

			//++++++++++++++++++++Hiding the bar graph from Switch function++++++++++++++++++++++++//
			d3.select(".chart"+s).attr("opacity",0);

			if(cou==3){
				d3.select("#"+biP.id).select(".edges").selectAll(".edge")
				.filter(function(d){
					return ((d.key1==p1) && (d.key2==p2) && d.h1 !=0 && d.h2 !=0);
				})
				.style("opacity",0.9);
			}
			else{
				if(s==0){
				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.filter(function(d){
					return ((d.key1==p1) && (d.key2==p2)&&(d.key3==p3) && d.h1 !=0 && d.h2 !=0);
				})
				.style("opacity",0.9);

				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.filter(function(d){
					return !((d.key1==p1) && (d.key2==p2)&&(d.key3==p3));
				})
				.style("opacity",0);
			 	}

			else{
				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.filter(function(d){
					return ((d.key1==p2) && (d.key2==p3)&&(d.key3==p1) && d.h1 !=0 && d.h2 !=0);
				})
				.style("opacity",0.9);

				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.filter(function(d){
					return !((d.key1==p2) && (d.key2==p3)&&(d.key3==p1));
				})
				.style("opacity",0);
				}
			}
			
		});
		
	}

	function restore(data){		
		data.forEach(function(biP,s){
			d3.select("#"+biP.id).select(".edges").selectAll(".edge").style("fill",function(d){
					return colors[d.key1];
			})
			.style("opacity",0.9);
		
			d3.select("#"+biP.id).select(".edges2").selectAll(".edge2").style("fill",function(d){
					return colors[d.key1];
			})
			.style("opacity",0);

			//++++++++++++++++++++Hiding the bar graph from Switch function++++++++++++++++++++++++//
			d3.select(".chart"+s).attr("opacity",0);
		});
	}

	function align33(data){

		
		data.forEach(function(biP,s){

			d3.select("#"+biP.id).select(".edges").selectAll(".edge").style("fill",function(d){
					return colors[d.key1];
				})
			.style("opacity",0);

			if(cou==4){
				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.filter(function(d){
					return ((d.key1 == d.key2) && (d.key2==d.key3) && d.h1 !=0 && d.h2 !=0);
				})
				.style("opacity",0.9);

				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.filter(function(d){
					return !((d.key1 == d.key2) && (d.key2==d.key3) && d.h1 !=0 && d.h2 !=0);
				})
				.style("opacity",0);
			}

			//++++++++++++++++++++Hiding the bar graph from Switch function++++++++++++++++++++++++//
			d3.select(".chart"+s).attr("opacity",0);

		});
			
	}



	function alignBy(data){
		
		data.forEach(function(biP,s){

			d3.select("#"+biP.id).select(".edges").selectAll(".edge").style("fill",function(d){
					return colors[d.key1];
				})
			.style("opacity",0.9);

			d3.select("#"+biP.id).select(".edges").selectAll(".edge")
			.filter(function(d){
				return (d.key1 != d.key2 && d.h1 != 0 && d.h2 != 0);
			})
			.style("opacity",0);
		
			if(cou==4){

				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.style("opacity",0);
			}

			//++++++++++++++++++++Hiding the bar graph from Switch function++++++++++++++++++++++++//
			d3.select(".chart"+s).attr("opacity",0);

		});
	}

	function star(data,x){
		
		data.forEach(function(biP,s){

			d3.select("#"+biP.id).select(".edges").selectAll(".edge").style("fill",function(d){
					return colors[d.key1];
				})
			.style("opacity",0.9);
			
			d3.select("#"+biP.id).select(".edges").selectAll(".edge")
			.filter(function(d){
				return !(d.key1 != x && d.key2 ==x && d.h1 !=0 && d.h2 !=0);
			})
			.style("opacity",0);

			if(cou==4){
				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.style("opacity",0);
			}

			//++++++++++++++++++++Hiding the bar graph from Switch function++++++++++++++++++++++++//
			d3.select(".chart"+s).attr("opacity",0);
			
		});
	}

	function slid(data,x){
		
		data.forEach(function(biP,s){
			
			d3.select("#"+biP.id).select(".edges").selectAll(".edge").style("fill",function(d){
					return colors[d.key1];
				})
			.style("opacity",0.9);

			d3.select("#"+biP.id).select(".edges").selectAll(".edge")
			.filter(function(d){
				return !(d.key1 == x && d.key2 !=x && d.h1 !=0 && d.h2 !=0);
			})
			.style("opacity",0);
			
			if(cou==4){
				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.style("opacity",0);
			}

			//++++++++++++++++++++Hiding the bar graph from Switch function++++++++++++++++++++++++//
			d3.select(".chart"+s).attr("opacity",0);
			
		});
	}

	function switchF(data,svg){
		
		
		data.forEach(function(biP,s){
			
			d3.select("#"+biP.id).select(".edges").selectAll(".edge").style("fill",function(d){
					return colors[d.key1];
				})
			.style("opacity",0.9);

			var initial_data=[['']],initial_data2=[['']];
			//console.log(data[0].data.data[0][1][1]);

			for (i=0; i<cou; i++)											
				{
					initial_data[i]=[];
					initial_data2[i]=[];
   					for (j=0; j<cou; j++)
   					{
							initial_data[i][j] = 0;
							initial_data2[i][j] = 0;
   					}
				}

			for (i=0; i<cou; i++)
				{
					for (j=0; j<cou; j++){
								if(i==j) continue;
								if(data[s].data.data[0][i][j] <=data[s].data.data[0][j][i]){
									initial_data[i][j]=data[s].data.data[0][i][j];
									initial_data[j][i] = data[s].data.data[0][i][j];
									initial_data2[j][i] = data[s].data.data[0][j][i] - data[s].data.data[0][i][j];
								}
								else{
									initial_data[i][j]=data[s].data.data[0][j][i];
									initial_data[j][i] = data[s].data.data[0][j][i];
									initial_data2[i][j] = data[s].data.data[0][i][j] - data[s].data.data[0][j][i];
								}
						}
					}

			// initial_data --> Contains the matrix for switch minimum
			// initial_data2 --> Contains the matrix for excess in switch

			//console.log(initial_data);
   			//console.log(initial_data2);
   			
   			d3.select("#"+biP.id).select(".edges").selectAll(".edge")
			.filter(function(d){
				return !(initial_data[d.key1][d.key2]);
				})
			.style("opacity",0);

			if(cou==4){
				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.style("opacity",0);
			}
			

			var k=0;
			var initial=[['']];
			for(i=0;i<cou;i++){
				for(j=0;j<cou;j++){
					if(initial_data2[i][j]) {
						initial[k]=[];
						initial[k][0]=i;
						initial[k][1]=initial_data2[i][j];
						initial[k][2]=j;
						k++; 
					}
				}
			}

			//console.log(initial);
			//transpose(initial);

			var width = 500,
				width1=200,
    			barHeight = 20;

			var x = d3.scale.linear()
    			.domain([0, d3.max(transpose(initial)[1])])
    			.range([0, width1]);

			var chart = d3.select(".chart"+s)
    			.attr("width", width)
    			.attr("height", barHeight * (transpose(initial)[1]).length)
    			.attr("opacity",0.9);
    
			var bar = chart.selectAll("g")
    			.data(initial)
  				.enter().append("g")
    			.attr("transform", function(d, i) { return "translate(" + 250 + "," + i * barHeight + ")"; });

			bar.append("text")
				.attr("x",function(d) { return (0- (width1/2)); })
				.attr("y",barHeight/2)
				.attr("dy", ".35em")
    			.text(function(d,i) { return remapp((transpose(initial))[2][i]); });

			bar.append("rect")
    			.attr("width", function(d,i) { return x((transpose(initial))[1][i]); })
		    	.attr("height", barHeight - 1);

			bar.append("text")
		    	.attr("x", function(d,i) { return x((transpose(initial))[1][i]) - 2; })
		    	.attr("y", barHeight / 2)
		    	.attr("dy", ".35em")
		    	.text(function(d,i) { return ((transpose(initial))[1][i]); });

			bar.append("text")
				.attr("x",function(d) { return width1 + 10; })
				.attr("y",barHeight/2)
				.attr("dy", ".35em")
    			.text(function(d,i) { return remapp((transpose(initial))[0][i]); });

		});
	}

	function voidS(data){

		data.forEach(function(biP,s){
			d3.select("#"+biP.id).select(".edges").selectAll(".edge")
			.style("opacity",0);
		
			if(cou==4){
				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.style("opacity",0);
			}
						
			d3.select("#"+biP.id).select(".edges").selectAll(".edge")
			.filter(function(d){
				return (d.h1 == 0 && d.h2 == 0);   
			})
			.attr("stroke","grey")
			.attr("stroke-width",2)
			.style("opacity",0.9);
		});
	}


	function returnP(data){

		data.forEach(function(biP,s){
			d3.select("#"+biP.id).select(".edges").selectAll(".edge")
			.style("opacity",0);
		
			if(s==0){
				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.filter(function(d){
					return ((d.key1 == d.key3) && (d.key1 !=d.key2) );
				})
				.style("opacity",0.9);

				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.filter(function(d){
					return !((d.key1 == d.key3) && (d.key1!=d.key2) );
				})
				.style("opacity",0);
			}
			else{
				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.filter(function(d){
					return ((d.key2 == d.key3) && (d.key1 !=d.key2) );
				})
				.style("opacity",0.9);

				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.filter(function(d){
					return !((d.key2 == d.key3) && (d.key1!=d.key2) );
				})
				.style("opacity",0);
			}
			
		});

	}

}();