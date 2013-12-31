	var circleRadius = 40;
	var circleXUnit = 100;
	var circleYUnit = 100;

	drawCircle = function(canvasCtx, xCenter, yCenter, radius){
		canvasCtx.beginPath();
		canvasCtx.arc(xCenter, yCenter, radius, 0,2*Math.PI);
		canvasCtx.stroke();
	}
	writeChordText = function(canvasCtx, xLoc, yLoc, chordText){
		canvasCtx.font = "bold 12px sans-serif";
		canvasCtx.fillText(chordText, xLoc, yLoc);
	}
	drawArrowHead = function(canvasCtx, xLocStart, yLocStart, size, direction){

	}
	drawArrow = function(canvasCtx, xLocStart, yLocStart, xLocEnd, yLocEnd){
		canvasCtx.beginPath();
		canvasCtx.moveTo(xLocStart, yLocStart);
		canvasCtx.lineTo(xLocEnd, yLocEnd);
      	canvasCtx.stroke();
	}
	drawArrowBetweenNodes= function(nodeStartX, nodeStartY, nodeEndX, nodeEndY){
		var c=document.getElementById("myCanvas");
		var ctx=c.getContext("2d");
		var circleRadiusX = circleRadius;
		var circleRadiusY = circleRadius;
		var nodesWrap = false;
		if (nodeStartX == nodeEndX){
			circleRadiusX = 0;
			if (Math.abs(nodeStartY - nodeEndY) > 1){
				nodesWrap = true;
			}

			if (nodeStartY > nodeEndY){
				circleRadiusY = circleRadiusY * -1;
			}
		}
		else if (nodeStartY == nodeEndY){
			circleRadiusY = 0;
			if (Math.abs(nodeStartX - nodeEndX) > 1){
				nodesWrap = true;
			}
			if (nodeStartX > nodeEndX){
				circleRadiusX = circleRadiusX * -1;
			}
		}

		var lineStartX = circleXUnit * (nodeStartX + .5) + circleRadiusX;
		var lineStartY = circleYUnit * (nodeStartY + .5) + circleRadiusY;
		var lineEndX = circleXUnit * (nodeEndX + .5) - circleRadiusX;
		var lineEndY = circleYUnit * (nodeEndY + .5) - circleRadiusY;

		
		if (nodesWrap == false){
			drawArrow(ctx, lineStartX, lineStartY, lineEndX, lineEndY);
			console.log("drawing arrow from indices: (" + nodeStartX + "," + nodeStartY + ")" + "(" + nodeEndX + "," + nodeEndY + "), and lineLocs: (" + lineStartX + "," + lineStartY + "),(" + lineEndX + "," + lineEndY + ")");
		}
		else{
			//draw dotted line toward the edge of the graph to indicate 
			//that the node graph wraps around
		}
	}
	buildChordNode = function(xIndex, yIndex, chordString){
		var c=document.getElementById("myCanvas");
		var ctx=c.getContext("2d");
		var circleCenterXLoc = circleXUnit * (xIndex + .5);
		var circleCenterYLoc = circleYUnit * (yIndex + .5);
		drawCircle(ctx, circleCenterXLoc, circleCenterYLoc, circleRadius);
		//write the chord name
		var estimatedTextSize = 44;
		writeChordText(ctx, circleCenterXLoc - (estimatedTextSize * .5), circleCenterYLoc, chordString);
		//draw arrows to neighbors
	}