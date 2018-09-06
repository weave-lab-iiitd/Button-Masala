#pragma once

#include "ofMain.h"
#include "ofxAruco.h"
#include "highlyreliablemarkers.h"
#include "ofxCircleMenuButton.h"
#include "ofxTimer.h"
class ofApp : public ofBaseApp{

	public:
        double calcDistance (int x1, int y1, int x2, int y2);
		void setup();
		void update();
		void draw();
        void metaData(vector<aruco::Marker> M);
    
        //void drawScreen();
		void keyPressed  (int key);
		void keyReleased(int key);
		void mouseMoved(int x, int y );
		void mouseDragged(int x, int y, int button);
		void mousePressed(int x, int y, int button);
		void mouseReleased(int x, int y, int button);
		void windowResized(int w, int h);
		void dragEvent(ofDragInfo dragInfo);
		void gotMessage(ofMessage msg);
    
    		//declaring menu object
		ofxCircleMenuButton menu;	
		
		ofVideoGrabber grabber;

		ofBaseVideoDraws * video;
		ofxTimer timer;
		ofxAruco aruco;
		bool showMarkers;
		//bool showBoard;
		//bool showBoardImage;
		//ofImage board;
		ofImage marker;
};
