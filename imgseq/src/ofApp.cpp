#include "ofApp.h"
#include "ofxCv.h"
#include "ofBitmapFont.h"

//--------------------------------------------------------------
void ofApp::setup(){    
    
    ofSetWindowTitle("ofxAruco - Highly Reliable Markers");
	ofSetVerticalSync(true);
        ofBackground(0,0,0);
    
    

	//setup cam parameters
	string cameraIntrinsics = "intrinsics.yml";
	string markerFile = "marker.xml";

	//setup video
	grabber.listDevices();
	grabber.setDeviceID(0);
	grabber.initGrabber(1920,1080);
	video = &grabber;
    
	
	
	//load marker
	aruco.setUseHighlyReliableMarker(markerFile);
	
	//init 
	aruco.setThreaded(true);
	aruco.setupXML(cameraIntrinsics, video->getWidth(), video->getHeight());

	showMarkers = true;
	ofEnableAlphaBlending();
    
    
    ofSetFrameRate(24.0);
    ofSetVerticalSync(true);
    
    ofSetLogLevel(OF_LOG_VERBOSE);
    mySequence.loadSequence("sequence",24.0f); // 24 FPS
   // mySequence.setShouldPingPong(true);
    mySequence.play();
    menu.setup();
    vector<string> menuItems;
	menuItems.push_back("1");
    menuItems.push_back("2");
    menuItems.push_back("3");
    menuItems.push_back("4");
    menuItems.push_back("5");
    menuItems.push_back("6");
    menuItems.push_back("7");
	menuItems.push_back("8");
	menuItems.push_back("9");
	menuItems.push_back("10");
	menuItems.push_back("11");
	menuItems.push_back("12");	
    menu.setMenuItems(menuItems);
}


//--------------------------------------------------------------
void ofApp::update(){
    video->update();
	if(video->isFrameNew()){
		aruco.detectBoards(video->getPixels());
	}
}

//--------------------------------------------------------------
void ofApp::draw(){
    mySequence.draw();
    aruco::Marker pointer;
	for (auto& m: aruco.getMarkers()) {
        if(m.id == 7)
        {
            pointer = m; 
        }     
	}
	for(auto& m: aruco.getMarkers())
	{
		if(m.id == pointer.id){
            ofSetColor(255, 255, 255);
            ofDrawCircle(m.getCenter().x, m.getCenter().y, 20);
            ofDrawCircle(m[0].x, m[0].y, 10);
            menu.set(m.getCenter().x, m.getCenter().y);
            //menu.draw();
            menu.set_index(m[0].x,m[0].y);
            mySequence.setCurrentFrameIndex(menu.get_index());
                     //ofDrawCircle(m[0].x, m[0].y, 10);
        }
	}
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){
    if(key == 'c')
        mySequence.setCurrentFrameIndex((mySequence.getCurrentFrameIndex() + 1)%30);
    else if (key == 'd')
        mySequence.setCurrentFrameIndex((mySequence.getCurrentFrameIndex() - 1 + 30)%30);
        
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y){

}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo){ 

}
