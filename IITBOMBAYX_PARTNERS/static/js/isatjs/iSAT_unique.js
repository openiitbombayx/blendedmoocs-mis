!function(){

	var bP={};	
	var b=30, bb=150, height=500, buffMargin=0, minHeight=14;
	var c1=[-95, 40], c2=[-50, 80], c3=[-10, 120]; //Column positions of labels.
	

	var colors = ["#a6cee3","#1f78b4","#b2df8a","#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","#cab2d6","#6a3d9a","#ffff99","#b15928"];

	bP.partData = function(data,p){
		var sData={};
		sData.keys=[
		d3.set(data.map(function(d){ return d[0];})).values(),   
		d3.set(data.map(function(d){ return d[1];})).values()    
		];
		
		sData.data = [	sData.keys[0].map( function(d){ return sData.keys[1].map( function(v){ return 0; }); }),
		sData.keys[1].map( function(d){ return sData.keys[0].map( function(v){ return 0; }); }) 
		];

		data.forEach(function(d){ 
			sData.data[0][sData.keys[0].indexOf(d[0])][sData.keys[1].indexOf(d[1])]=d[p];
			sData.data[1][sData.keys[1].indexOf(d[1])][sData.keys[0].indexOf(d[0])]=d[p]; 
		});
		return sData;
	}
	
	function visualize(data,col){
		var vis ={};
		//console.log(data);
		function calculatePosition(a, s, e, b, m){
			//console.log(a);

			var total=d3.sum(a);
			var sum=0, neededHeight=0, leftoverHeight= e-s-2*b*a.length;
			var ret =[];

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
			//console.log("1");
			return ret;
		}
		//console.log(data.data[0].map(function(d){ return d3.sum(d);}));
		//console.log(data.data[1].map(function(d){ return d3.sum(d);}));
		vis.mainBars = [ 
		calculatePosition( data.data[0].map(function(d){ return d3.sum(d);}), 0, height, buffMargin, minHeight),
		calculatePosition( data.data[1].map(function(d){ return d3.sum(d);}), 0, height, buffMargin, minHeight)
		];
		
		//console.log(data.data[0].map(function(d){ return d3.sum(d);})); // ------------------------> An array of number's frequencies

		vis.subBars = [[],[]];
		vis.mainBars.forEach(function(pos,p){
			pos.forEach(function(bar, i){	
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

		if(cou==4){
		//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//

		// Array crr contains the breakdown of subBars[0] frequency to calculate further sub-subBars
		
		//console.log(unikc[col].length);
		//console.log(unikc[col+1].length);
		var temp;
		var crr=[['']],q=0;
		for(i=0;i<unikc[col].length;i++){
			for(j=0;j<unikc[col+1].length;j++){
				crr[q]= srch(i,j,col);
				q++;	
			}
		}

		function srch(i,j,s){
			var srr=[];
			
			if(s==0){
				for(k=0;k<unikc[2].length;k++) srr[k]=0;
					for(k=0;k<nArray.length;k++){
						if(nArray[k][0]==i && nArray[k][1]==j) srr[nArray[k][2]] = nArray[k].deepSortAlpha;
					}
				}
				else{
					for(k=0;k<unikc[0].length;k++) srr[k]=0;
						for(k=0;k<nArray.length;k++){
							if(nArray[k][1]==i && nArray[k][2]==j) srr[nArray[k][0]] = nArray[k].deepSortAlpha;
						}
					}
					return srr;

				}
		//console.log(crr);

		vis.subBars2 = [[ ],[ ]];                            //an array containing the sub-subBars

		//console.log(vis.subBars);
		//console.log(crr);


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
				h2:vis.subBars2[1][i].h,
				value:p.value
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
		h2:vis.subBars[1][i].h,
		value:p.value,
	};
});
vis.keys=data.keys;
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
			d3.select("#"+id).select(".part"+p).append("g").attr("class","subbars2");                   
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
			.text(function(d,i){return remapp(data.keys[p][i],p+s); })
			.attr("text-anchor","start" );
			
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
					if(data.edges[i].h1 !=0 && data.edges[i].h2 !=0){
						if(p==0)sum2 += data.edges[i].value;
						else sum2 += data.edges[i].value;

					}
				}

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

		// Tooltip //
		div = d3.select("#tabpage_2").append("div")	
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
			div	.html("count "+ d.value + "<br/>")	
			// .style("left", (d3.event.pageX) + "px")		
			// .style("top", (d3.event.pageY) + "px");	
			;
		})					
		.on("mouseout", function(d) {		
			div.transition()		
			.duration(500)		
			.style("opacity", 0);	
		});  
	}	
	
	function drawHeader(header, id){
		
		d3.select("#"+id).append("g").attr("class","header").append("text").text(header[2])
		.style("font-size","14").attr("x",108).attr("y",-20).style("text-anchor","middle").style("fill","grey")
		;
		
		[0,1,2].forEach(function(d){
			var h = d3.select("#"+id).select(".part"+d).append("g").attr("class","header");
			
			h.append("text").text(header[d]).attr("x", (c1[d]-5))
			.attr("y", -5).style("fill","orange")
			.style("font-weight","bold");
			
		});
	}
	
	function drawFooter(sum2,id){

		d3.select("#"+id).append("g").attr("class","footer").append("text").text(sum2)
		.style("font-size","14").attr("x",108).attr("y",20+height).style("text-anchor","middle")
		.style("font-weight","bold");
	}
	
	function transitionFooter(sum2,id){
		d3.select("#"+id).select(".footer").transition().duration(500).text(sum2);
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

		mainbar.select(".labelvalue1").transition().duration(500)
		.text( sum1 );

		var sum2=0;
		for(i=0;i<data.edges.length;i++){
			if(data.edges[i].h1 !=0 && data.edges[i].h2 !=0){
				if(p==0) sum2 += data.edges[i].value;
				else
					sum2 += data.edges[i].value;					
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

		// Define the div for the tooltip
		

		d3.select("#"+id).select(".edges").selectAll(".edge").data(data.edges)
		.on("mouseover", function(d) {		
			div.transition()		
			.duration(200)		
			.style("opacity", .9);		
			div.html(d.value + "<br/>")	
			.style("left", (d3.event.pageX) + "px")		
			.style("top", (d3.event.pageY) + "px");	
		})					
		.on("mouseout", function(d) {		
			div.transition()		
			.duration(500)		
			.style("opacity", 0);	
		});
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
		.text(function(d,i) { return remapp((transpose(initial))[0][i],0); });

		bar.append("rect")
		.attr("width", function(d,i) { return x((transpose(initial))[1][i]); })
		.attr("height", barHeight - 10);

		bar.append("text")
		.attr("x", function(d,i) { return x((transpose(initial))[1][i]) - (.025*x((transpose(initial))[1][i])); })
		.attr("y", barHeight / 2)
		.attr("dy", ".35em")
		.text(function(d,i) { return ((transpose(initial))[1][i]); });

	} 

	function addText(dat){

		var width = 500,
		height = 40;

		var svg = d3.select("#textL").append("svg")
		.attr("width", width)
		.attr("height", height)
		.append("g")
    	.attr("transform", "translate(0," + (height / 2) + ")");


  function update(data) {

  		// DATA JOIN
  		// Join new data with old elements, if any.
  		var text = svg.selectAll("text")
  		.data(data);

  		// UPDATE
  		// Update old elements as needed.
  		//text.attr("class", "update");

  		// ENTER
  		// Create new elements as needed.
  		text.enter().append("text")
      		//.attr("class", "enter")
      		.attr("x", function(d, i) { return i * 8; })
      		.attr("dy", ".35em");

  		// ENTER + UPDATE
  		// Appending to the enter selection expands the update selection to include
  		// entering elements; so, operations on the update selection after appending to
  		// the enter selection will apply to both entering and updating nodes.
  		text.text(function(d) { return d; });

  		// EXIT
  		// Remove old elements as needed.
  		text.exit().remove();
  	}

		// The initial display.
		update(dat);
	}

	bP.draw2 = function(data,svg){
		var m=0;
		data.forEach(function(biP,s){
			svg.append("g")
			.attr("id", biP.id)
			.attr("transform","translate("+ (310*s+11*max*s)+",0)");

	//-----------------------------------Drawing the Bars and Edges for the Graph-----------------------------------//
	var visData = visualize(biP.data,s);                          
	drawPart(visData, biP.id, 0,s);
	drawPart(visData, biP.id, 1,s);
	drawEdges(visData, biP.id,s);
	drawHeader(biP.header, biP.id);

/*
			var i,sum2=0;
			for(i=0;i<visData.edges.length;i++)	if(visData.edges[i].h1 !=0 && visData.edges[i].h2 !=0)sum2 += visData.edges[i].value;					

			drawFooter(sum2,biP.id);
		*/
			// For drawing the 5th bar
			if(s>0 || cou==3){
				svg.append("g")										
				.attr("id", 'Last')
				.attr("transform","translate("+ ((220*(s+1))+11*max*(s+1))+",0)");
				drawPart(visData, 'Last', 1,s);
			}

	//---------------------------Defining the interactivity for edges and tooltip-----------------------------------//

	if(cou>3){
		d3.select("#"+biP.id).select(".edges").selectAll(".edge")
		.on("click",function(d,i){
					//d3.select(this).style("fill", "black");
					return plot(data,d,i,s);});
	}

	//--------------------------------------------Defining the interactivity for Bars---------------------------//
	
	[0,1].forEach(function(p){	                                  	
		d3.select("#"+biP.id)
		.select(".part"+p)
		.select(".mainbars") 
		.selectAll(".mainbar")
		.on("click",function(d, i){ return bP.selectSegment(data,s,i,p); })
	});

	var d;
	if(cou==3)d=1;
	else d=1;

	[1].forEach(function(p){	                                  	
		d3.select("#"+"Last")
		.select(".part"+(1))
		.select(".mainbars") 
		.selectAll(".mainbar")
		.on("click",function(d, i){ return bP.selectSegment(data,1,i,1); })
	});


	//----------------------------------Patterns and HTML Elements----------------------------------------------//
	
	// document.getElementById("restore1").ondblclick = function() {
	// 	restore(data,0);
	// 	return bP.deSelectSegment(data, s, i);
	// };
	// document.getElementById("align3").onclick = function() { align33(data,visData)};    			
	// document.getElementById("align2").onclick = function() { alignBy(data,visData)};
	// document.getElementById("starBurst").onclick = function() { starburstP(data,visData)};
	// document.getElementById("slide").onclick = function() { slideP(data,visData)};
	// 		document.getElementById("attr").onclick = function() { clickAttr(data,1,s,visData)};       //Setting p=1 since transition would occur to second bar only
	// 		document.getElementById("voidS").onclick = function() { voidS(data,visData)};
	// 		document.getElementById("switch").onclick = function() { switchF(data,svg,visData);};
	// 		document.getElementById("ePattern").onclick = function() { enterP(data,visData)}; 
	// 		document.getElementById("returnP").onclick = function() { returnP(data,visData)};
		});			
}

function transpose(a) {
	return Object.keys(a[0]).map(function (c) {
		return a.map(function (r) {
			return r[c];
		});
	});
}



bP.selectSegment = function(data, s1, i,p){

	bP.deSelectSegment(data,s1,i);

	data.forEach(function(biP,s){

			d3.select(".chart"+s).attr("opacity",0);	//Hiding the bar graph of Switch function

			if(cou==3){
				restore(data,0);
				if(p==0){
					d3.select("#"+biP.id).select(".edges").selectAll(".edge")
					.filter(function(d){
						return ((d.key1 !=i) && d.h1 !=0 && d.h2 !=0);
					})
					.style("fill","grey");

					d3.select("#"+biP.id).select(".part"+s).select(".subbars")
					.selectAll(".subbar")
					.filter(function(d){
						return ((d.key1!=i) && d.h1 !=0 && d.h2 !=0);
					})
					.style("fill","grey");


					d3.select("#"+biP.id).select(".part"+(1-s)).select(".subbars")
					.selectAll(".subbar")
					.filter(function(d){
						return ((d.key1 !=i) && d.h1 !=0 && d.h2 !=0);
					})
					.style("fill","grey");

				}
				else{
					d3.select("#"+biP.id).select(".edges").selectAll(".edge")
					.filter(function(d){
						return ((d.key2 !=i) && d.h1 !=0 && d.h2 !=0);
					})
					.style("fill","grey");

					d3.select("#"+biP.id).select(".part"+s).select(".subbars")
					.selectAll(".subbar")
					.filter(function(d){
						return  ((d.key2!=i) && d.h1 !=0 && d.h2 !=0);
					})
					.style("fill","grey");

					d3.select("#"+biP.id).select(".part"+(1-s)).select(".subbars")
					.selectAll(".subbar")
					.filter(function(d){
						return ((d.key2!=i) && d.h1 !=0 && d.h2 !=0);
					})
					.style("fill","grey");

					d3.select("#"+'Last').select(".part"+(s)).select(".subbars")
					.selectAll(".subbar")
					.filter(function(d){
						return ((d.key2!=i) && d.h1 !=0 && d.h2 !=0);
					})
					.style("fill","grey");
				}
			}
			else{restore(data,1);
				if(s1==0 && p==0){
					if(s==0){
						d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
						.filter(function(d){
							return ((d.key1!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");

						d3.select("#"+biP.id).select(".part"+s).select(".subbars2")
						.selectAll(".subbar2")
						.filter(function(d){
							return ((d.key1!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");


						d3.select("#"+biP.id).select(".part"+(1-s)).select(".subbars2")
						.selectAll(".subbar2")
						.filter(function(d){
							return ((d.key1!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");



					}	

					else{
						d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
						.filter(function(d){
							return ((d.key3 !=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");

						d3.select("#"+biP.id).select(".part"+s).select(".subbars2")
						.selectAll(".subbar2")
						.filter(function(d){
							return ((d.key3!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");


						d3.select("#"+biP.id).select(".part"+(1-s)).select(".subbars2")
						.selectAll(".subbar2")
						.filter(function(d){
							return ((d.key3!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");


						d3.select("#"+'Last').select(".part"+(s)).select(".subbars2")
						.selectAll(".subbar2")
						.filter(function(d){
							return ((d.key3!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");

					}

				}
				else if(s1==1 && p==1){
					if(s==1){
						d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
						.filter(function(d){
							return ((d.key2!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");

						d3.select("#"+biP.id).select(".part"+s).select(".subbars2")
						.selectAll(".subbar2")
						.filter(function(d){
							return ((d.key2!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");


						d3.select("#"+biP.id).select(".part"+(1-s)).select(".subbars2")
						.selectAll(".subbar2")
						.filter(function(d){
							return ((d.key2!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");

						d3.select("#"+'Last').select(".part"+(s)).select(".subbars2")
						.selectAll(".subbar2")
						.filter(function(d){
							return ((d.key2!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");
					}

					else{
						d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
						.filter(function(d){
							return ((d.key3!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");

						d3.select("#"+biP.id).select(".part"+s).select(".subbars2")
						.selectAll(".subbar2")
						.filter(function(d){
							return ((d.key3!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");


						d3.select("#"+biP.id).select(".part"+(1-s)).select(".subbars2")
						.selectAll(".subbar2")
						.filter(function(d){
							return ((d.key3!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");
					}

				}
				else{
					if(s==0){
						d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
						.filter(function(d){
							return ((d.key2!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");

						d3.select("#"+biP.id).select(".part"+s).select(".subbars2")
						.selectAll(".subbar2")
						.filter(function(d){
							return ((d.key2!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");


						d3.select("#"+biP.id).select(".part"+(1-s)).select(".subbars2")
						.selectAll(".subbar2")
						.filter(function(d){
							return ((d.key2!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");
					}

					else{
						d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
						.filter(function(d){
							return ((d.key1!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");

						d3.select("#"+biP.id).select(".part"+s).select(".subbars2")
						.selectAll(".subbar2")
						.filter(function(d){
							return ((d.key1!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");


						d3.select("#"+biP.id).select(".part"+(1-s)).select(".subbars2")
						.selectAll(".subbar2")
						.filter(function(d){
							return ((d.key1!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");

						d3.select("#"+'Last').select(".part"+(s)).select(".subbars2")
						.selectAll(".subbar2")
						.filter(function(d){
							return ((d.key1!=i) && d.h1 !=0 && d.h2 !=0);
						})
						.style("fill","grey");
					}

				}
			}	
			
		});



}


bP.deSelectSegment = function(data, m, s){
	data.forEach(function(biP,s){
		if(cou==3){
			d3.select("#"+biP.id).select(".edges").selectAll(".edge")
			.style("fill",function(d){ return colors[d.key1];});

			d3.select("#"+biP.id).select(".part"+(0)).select(".subbars")
			.selectAll(".subbar")
			.style("fill",function(d){ return colors[d.key1];});


			d3.select("#"+biP.id).select(".part"+(1)).select(".subbars")
			.selectAll(".subbar")
			.style("fill",function(d){ return colors[d.key1];});

			d3.select("#"+'Last').select(".part"+(1)).select(".subbars")
			.selectAll(".subbar")
			.style("fill",function(d){ return colors[d.key2];});
		}
		else{

			d3.select("#"+biP.id).select(".edges").selectAll(".edge")
			.style("fill",function(d){ return colors[d.key1];});


			d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
			.style("fill",function(d){ return colors[d.key1];});

			d3.select("#"+biP.id).select(".part"+(0)).select(".subbars2")
			.selectAll(".subbar2")
			.style("fill",function(d){ return colors[d.key1];});


			d3.select("#"+biP.id).select(".part"+(1)).select(".subbars2")
			.selectAll(".subbar2")
			.style("fill",function(d){ return colors[d.key1];});

			d3.select("#"+'Last').select(".part"+(1)).select(".subbars2")
			.selectAll(".subbar2")
			.style("fill",function(d){ return colors[d.key2];});
		}



	});
}



function plot(data,d,n,q){
	if(q==0) return plot1(data,d,n);
	else return plot2(data,d,n);

}

function plot1(data,d,n){
	var newdata =  {keys:[], data:[]};
	data.forEach(function(k,x){
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

			var s_data3 = cal_frq(initial_data,1,0);
				//console.log(s_data3);
				newdata.data[0] = s_data3.map( function(d){ return d;});

				//+++++++++++++++++++++++++++++++++++++++//
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

				var s_data3 = cal_frq(initial_data,1,0);
				//console.log(s_data3);
				newdata.data[1] = transpose(s_data3);

			}
			else
			{	
				var initial_data2 = [['']];
				for (i=0,j=0; i<combined_data.length; i++)
				{
					temp2 = parseInt(combined_data[i][2]);
					if(temp2 != d.key2)continue;
					initial_data2[j]=[];
					initial_data2[j][0] = parseInt(combined_data[i][0]);
					initial_data2[j][1] = parseInt(combined_data[i][1]);
					initial_data2[j][2] = parseInt(combined_data[i][2]);
					j++;

				}

				var s_data3 = cal_frq(initial_data2,1,0);
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

					var s_data3 = cal_frq(initial_data,1,1);	
					//console.log(s_data3);

					//newdata.data[1] = s_data3.map( function(d){ return d;});
					newdata.data[1] = transpose(s_data3);
				}
			transition(visualize(newdata,x), k.id,x);                  //1st- for newData-0 and 2nd- for newData-1
		});
transition(visualize(newdata,1),'Last',x);


}

function plot2(data,d,n){
	var newdata =  {keys:[], data:[]};
	data.forEach(function(k,x){

		var a=x;
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

			var s_data3 = cal_frq(initial_data2,1,1);
				//console.log(s_data3);
				newdata.data[0] = s_data3.map( function(d){ return d;});

				//+++++++++++++++++++++++++++++++//
				
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

				var s_data3 = cal_frq(initial_data,1,0);
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

				var s_data3 = cal_frq(initial_data,1,0);	
				newdata.data[0] = s_data3.map( function(d){ return d;});
					//console.log(newdata.data[1-m]);

					//++++++++++++++++++++++++++++++++++++++++//
					var initial_data = [['']];
					for (i=0,j=0; i<combined_data.length; i++)
					{

						temp2 = parseInt(combined_data[i][2]);
						if(temp2 != d.key1)continue;
						initial_data[j]=[];
						initial_data[j][0] = parseInt(combined_data[i][0]);
						initial_data[j][1] = parseInt(combined_data[i][1]);
						initial_data[j][2] = parseInt(combined_data[i][2]);
						j++;

					}

					var s_data3 = cal_frq(initial_data,1,1);
					//console.log(s_data3);
					newdata.data[1] = transpose(s_data3);//.map( function(d){ return d;});
				}

				transition(visualize(newdata,1), k.id,x);
				transition(visualize(newdata,1),'Last',x);
			});
}


this.bP = bP;



	//********************************************PATTERNS******************************************//
							//*****************Onto same diagram******************//

							function clickAttr(data,p,s,visData){
								console.log("For Attractive Pattern");
								if(cou==3){
			var val1 = prompt("Enter the criteria value for 1st phase");   //belong to phase two so 1 is used in mapp function
			star(data,mapp(val1,1),mapp(val1,1),visData);
		}
		else{
			var val1 = prompt("Enter the criteria value for 1st phase");   //belong to phase two so 1 is used in mapp function
			var val2 = prompt("Enter the criteria value for 2nd phase");   //belong to phase three so 2 is used in mapp function
			star(data,mapp(val1,1),mapp(val2,2),visData);
		}
		

	}

	function starburstP(data,visData){
		var x1 = prompt("Enter the value for which you wish to see the startburst");
		console.log("For Starburst Pattern");
		if(cou==3) star(data,mapp(x1,1),mapp(x1,1),visData);
		else star(data,mapp(x1,1),mapp(x1,2),visData);
	}

	function slideP(data,visData){
		var x1 = prompt("Enter the value from which you wish to observe the slide in Phase1,eg. fail etc.");
		console.log("For Slide Pattern");
		if(cou==3) slid(data,mapp(x1,1),mapp(x1,1),visData);
		else slid(data,mapp(x1,1),mapp(x1,2),visData);
	}

	function star(data,x1,x2,visData){
		

		data.forEach(function(biP,s){

			d3.select("#"+biP.id).select(".edges").selectAll(".edge").style("fill",function(d){
				return colors[d.key1];
			})
			.style("opacity",0.9);
			
			if(s==0) x=x1;
			else x=x2;
			d3.select("#"+biP.id).select(".edges").selectAll(".edge")
			.filter(function(d){
				return !(d.key1 != x && d.key2 ==x );
			})
			.style("opacity",0);

			if(cou==4){
				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.style("opacity",0);
			}
			
			d3.select(".chart"+s).attr("opacity",0);	//Hiding the bar graph of Switch function	
			
		});

		//Calculations for Starburst pattern
		var sum1;
		var i,j;
		for(j=0;j<cou-2;j++){
			sum1=0
			for(i=0;i<nArray.length;i++){
				if(nArray[i][j+1]==x && nArray[i][j] !=x) sum1+= nArray[i].deepSortAlpha;
			}
			console.log(sum1);

		}
	}

	function slid(data,x1,x2,visData){
		
		data.forEach(function(biP,s){
			
			d3.select("#"+biP.id).select(".edges").selectAll(".edge").style("fill",function(d){
				return colors[d.key1];
			})
			.style("opacity",0.9);

			if(s==0) x=x1;
			else x=x2;

			d3.select("#"+biP.id).select(".edges").selectAll(".edge")
			.filter(function(d){
				return !(d.key1 == x && d.key2 !=x && d.h1 !=0 && d.h2 !=0);
			})
			.style("opacity",0);
			
			if(cou==4){
				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.style("opacity",0);
			}

			d3.select(".chart"+s).attr("opacity",0);	//Hiding the bar graph of Switch function			
		});

		//Calculations for Slide pattern
		var sum1;
		var i,j;
		for(j=0;j<cou-2;j++){
			sum1=0
			for(i=0;i<nArray.length;i++){
				if(nArray[i][j]==x && nArray[i][j+1] !=x) sum1+= nArray[i].deepSortAlpha;
			}
			console.log(sum1);
		}
	}

	function enterP(data,visData){
		var p1 = prompt("Enter the 1st value");
		var p2 = prompt("Enter the 2nd value");
		if(cou==4){
			var p3 = prompt("Enter the 3rd value");
			p3 = mapp(p3,2);
		} 

		p1 = mapp(p1,1);
		p2 = mapp(p2,1);
		
		data.forEach(function(biP,s){
			d3.select("#"+biP.id).select(".edges").selectAll(".edge")
			.style("opacity",0);

			
			d3.select(".chart"+s).attr("opacity",0);	//Hiding the bar graph of Switch function

			if(cou==3){
				d3.select("#"+biP.id).select(".edges").selectAll(".edge")
				.filter(function(d){
					return (d.h1 !=0 && d.h2 !=0 && (d.key1==p1) && (d.key2==p2));
				})
				.style("opacity",0.9);
			}
			else{
				if(s==0){
					d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
					.filter(function(d){
						return (d.h1 !=0 && d.h2 !=0 && (d.key1==p1) && (d.key2==p2)&&(d.key3==p3));
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
						return (d.h1 !=0 && d.h2 !=0 && (d.key1==p2) && (d.key2==p3)&&(d.key3==p1));
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

		//calculations for enter pattern
		var sum1=0,i,j;
		if(cou==3){
			for(i=0;i<nArray.length;i++){
				if(nArray[i][0]== p1 && nArray[i][1]==p2) {
					sum1=nArray[i].deepSortAlpha;		
					break;	
				}
			} 
		} 
		else{
			for(i=0;i<nArray.length;i++){
				if(nArray[i][0]== p1 && nArray[i][1]==p2 && nArray[i][2]==p3){
					sum1=nArray[i].deepSortAlpha;		
					break;	
				} 
			} 
		} 
		console.log("For EnterPattern");
		console.log(sum1);
		var text_pattern= sum1+' transitions follow this pattern';
		addText(text_pattern);
	}

	function restore(data,i){		
		data.forEach(function(biP,s){
			if(i==0){
				d3.select("#"+biP.id).select(".edges").selectAll(".edge")
				.style("opacity",0.9);

				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.style("opacity",0);

			}
			else{
				d3.select("#"+biP.id).select(".edges").selectAll(".edge")
				.style("opacity",0);

				d3.select("#"+biP.id).select(".edges2").selectAll(".edge2")
				.style("opacity",0.9);

			}
			
			d3.select(".chart"+s).attr("opacity",0);	//Hiding the bar graph of Switch function
			
		});
	}

	function align33(data,visData){

		
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
			d3.select(".chart"+s).attr("opacity",0);	//Hiding the bar graph of Switch function
		});

		//+++++++++++++++++++++++Calculating count for aligned3 pattern++++++++++++++++++++++++++++//
		var sum=0
		var i,j;
		for(i=0;i<nArray.length;i++){
			if(nArray[i][0]==nArray[i][1] && nArray[i][1]== nArray[i][2]) sum += nArray[i].deepSortAlpha;
		}
		console.log("For Align-3 Pattern");
		console.log(sum);
		var text_align3= ""+sum+" are aligned across the 3 phases in their respective stratum.";
		addText(text_align3);	
	}

	function alignBy(data,visData){
		console.log("For Align-2 Pattern");
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

			d3.select(".chart"+s).attr("opacity",0);	//Hiding the bar graph of Switch function
		});

		//Calculations for Align-2 Phase pattern
		var sum1;
		var i,j;
		for(j=0;j<cou-2;j++){
			sum1=0
			for(i=0;i<nArray.length;i++){
				if(nArray[i][j]==nArray[i][j+1]) sum1+= nArray[i].deepSortAlpha;
			}
			
			console.log(sum1);
			var text_align2= ""+sum1+" are aligned across the 2 phases in their respective stratum.";
			addText(text_align2);	
		// alert(text_align2);

	}
}



function switchF(data,svg,visData){


	data.forEach(function(biP,s){

		d3.select("#"+biP.id).select(".edges").selectAll(".edge").style("fill",function(d){
			return colors[d.key1];
		})
		.style("opacity",0.9);

		var initial_data=[['']],initial_data2=[['']];

		for (i=0; i<unikc[s].length; i++)											
		{
			initial_data[i]=[];
			initial_data2[i]=[];
			for (j=0; j<unikc[s+1].length; j++)
			{
				initial_data[i][j] = 0;
				initial_data2[i][j] = 0;
			}
		}

		for (i=0; i<unikc[s].length; i++)
		{
			for (j=0; j<unikc[s+1].length; j++){
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

			// console.log(initial_data);
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
   			for(i=0;i<unikc[s].length;i++){
   				for(j=0;j<unikc[s+1].length;j++){
   					if(initial_data[i][j]) {
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
			.text(function(d,i) { return remapp((transpose(initial))[2][i],s); });

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
			.text(function(d,i) { return remapp((transpose(initial))[0][i],s+1); });

		});
}

function voidS(data,visData){

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

			d3.select(".chart"+s).attr("opacity",0);	//Hiding the bar graph of Switch function			
		});
}


function returnP(data,visData){

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
			d3.select(".chart"+s).attr("opacity",0);	//Hiding the bar graph of Switch function			
		});
		//calculations for returnP
		var temp,i,j;
		for(i=0;i<nArray.length;i++){
			if(nArray[i][0]== nArray[i][2] && nArray[i][0] != nArray[i][1]) {
				console.log(remapp(nArray[i][0],0)+ "->" + remapp(nArray[i][1],1) + "->" + remapp(nArray[i][2],2) + " count = "+ nArray[i].deepSortAlpha);
				// var text_return="+remapp(nArray[i][0],0)+ ->  count = +nArray[i].deepSortAlpha+";
				// addText(text_pattern);
				alert(remapp(nArray[i][0],0)+ "->" + remapp(nArray[i][1],1) + "->" + remapp(nArray[i][2],2) + " count = "+ nArray[i].deepSortAlpha)
			}
		}

	}





}();