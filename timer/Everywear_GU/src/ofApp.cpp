#include "ofApp.h"
#include "ofxCv.h"
#include "ofBitmapFont.h"
#include <math.h>
#include "ofMain.h"
#include "ofxCircleMenuButton.h"

double calcDistance (int x1, int y1, int x2, int y2){
    int distancex = (x2 - x1)^2;
    int distancey = (y2 - y1)^2;
    double calcdistance = sqrt(distancex - distancey);
    return calcdistance;
    
}

void drawMarker(float size, const ofColor & color, vector<aruco::Marker> M){
	//ofDrawAxis(size);
    /*
    for (auto& m: M) {
        ofDrawCircle(m.getCenter().x, m.getCenter().y, 10);
    }
    */
    
   // ofDrawCircle(<#const glm::vec2 &p#>, size)
    //ofDrawB
	/*
    ofPushMatrix();
		// move up from the center by size*.5
		// to draw a box centered at that point
		ofTranslate(0,size*0.5,0);
		ofFill();
		ofSetColor(color,50);
		ofDrawBox(size);
		ofNoFill();
		ofSetColor(color);
		ofDrawBox(size);
	ofPopMatrix();
     */
    
}

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
       //Setup Timer
	timer.setup();

       //Setup Menu
	menu.setup();
        vector<string> menuItems;
        menuItems.push_back("0");
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
        timer.update();
	video->update();
	if(video->isFrameNew()){
		aruco.detectBoards(video->getPixels());
	}
}

//--------------------------------------------------------------
void ofApp::draw(){
	
	ofSetColor(255);
	timer.draw();
	menu.draw();
	//ofDrawCircle(mouseX, mouseY, 20);
	video->draw(video->getWidth(),0,-video->getWidth(),video->getHeight());// Prints the video on the screen(window)
   	 if(showMarkers){
		for(int i=0;i<aruco.getNumMarkers();i++){
			aruco.begin(i);
			drawMarker(0.15, ofColor::white, aruco.getMarkers());
			aruco.end();
		}
	}
    
    int flag=0;
    //metaData(aruco.getMarkers());
    aruco::Marker pointer;
	for (auto& m: aruco.getMarkers()) {
		//cout << m.getArea() << endl;
        if(m.id == 7)
        {
            pointer = m; //Aruco_7 is the pointer
        }
        
	}
    
    for(auto& m: aruco.getMarkers()) {
        ofSetColor(255);
        if(m.id == 5)
        {
            ofSetColor(0, 255, 0);
            ofDrawCircle(m.getCenter().x, m.getCenter().y, 50);
            ofSetColor(255, 255, 255);
            ofDrawBitmapString("Hours" ,m.getCenter().x, m.getCenter().y);
        }
        else if(m.id == 2)
        {
            ofSetColor(255, 0, 0);
            ofDrawCircle(m.getCenter().x, m.getCenter().y, 50);
            ofSetColor(255, 255, 255);
            ofDrawBitmapString("Min" ,m.getCenter().x, m.getCenter().y);
        }
        else if(m.id == 6)
        {
            ofSetColor(0, 0, 255);
            ofDrawCircle(m.getCenter().x, m.getCenter().y, 50);
            ofSetColor(255, 255, 255);
            ofDrawBitmapString("Sec" ,m.getCenter().x, m.getCenter().y);
        }
        else if(m.id == pointer.id){
            ofSetColor(255, 255, 255);
            ofDrawCircle(m.getCenter().x, m.getCenter().y, 20);
                     //ofDrawCircle(m[0].x, m[0].y, 10);
        }
       // else
           // ofDrawCircle(m.getCenter().x, m.getCenter().y, 50);
        cout<<m.id<<endl;
        ofSetColor(255);
        int distancex = (int)pow(m.getCenter().x - pointer.getCenter().x, 2);
        int distancey = (int)pow(m.getCenter().y - pointer.getCenter().y, 2);
        double calcdistance = sqrt(distancex - distancey);
        ofDrawBitmapString(ofToString(m.id) + " " +ofToString(calcdistance),m.getCenter().x + 30, m.getCenter().y+ 30);
	//Condition if distance is less than threshold
    /*
	if(calcdistance <= 200  && m.id != 0 )
        {
            //ofSetColor(20);
            //ofDrawCircle(m.getCenter().x, m.getCenter().y, 100);
            ofSetColor(255);
            ofDrawCircle(m.getCenter().x, m.getCenter().y, 50);
            ofDrawBitmapString(ofToString(m.id) + " " +ofToString(calcdistance),m.getCenter().x + 15, m.getCenter().y + 15);
            //Enabel menu settings
	        menu.set(m.getCenter().x, m.getCenter().y);
            menu.set_index(m[0].x,m[0].y);
            if(m.id==1 && menu.get_index()!=-1)timer.set_hours(menu.get_index() +1);
            else if(m.id==2 && menu.get_index()!=-1)timer.set_minutes(menu.get_index());
            else if(m.id==3 && menu.get_index()!=-1)timer.set_seconds(menu.get_index());
        }
	else { menu.reset();}
       */
    if(calcdistance <= 250 &&(m.id == 2 || m.id == 5 || m.id == 6) && calcdistance >= 10)
    {
        cout<<"yo";
         menu.set(m.getCenter().x, m.getCenter().y);
         //menu.draw();
         menu.set_index(m[0].x,m[0].y);
        ofDrawCircle(m[0].x, m[0].y, 10);
         if(m.id==5 && menu.get_index()!=-1)timer.set_hours(menu.get_index() % 12);
         else if(m.id==2 && menu.get_index()!=-1)timer.set_minutes(menu.get_index() % 12);
         else if(m.id==6 && menu.get_index()!=-1)timer.set_seconds(menu.get_index() % 12);
        flag=1;
        
    }
    else // if (flag==0)
    {
        menu.reset();
        
    }
        
    }
    int button_x=timer.get_buttonx();
    int button_y=timer.get_buttony();
    double b_distance= sqrt(pow(pointer.getCenter().x-button_x,2)+pow(pointer.getCenter().y-button_y,2));
    if(b_distance <100)timer.set_start();
    
	ofSetColor(255);
	ofDrawBitmapString("markers detected: " + ofToString(aruco.getNumMarkers()),20,20);
	ofDrawBitmapString("fps " + ofToString(ofGetFrameRate()),20,40);
	ofDrawBitmapString("m toggles markers",20,60);


}

/*
void metaData(vector<aruco::Marker> M)
{
    for (auto& m: M) {
        cout<<m.id<<endl;
        ofDrawBitmapString(ofToString(m.id),m.getCenter().x + 10, m.getCenter().y + 10);
    }
}

void ofApp::drawScreen(){
    
}
*/

//--------------------------------------------------------------
void ofApp::keyPressed(int key){
	if(key=='m') showMarkers = !showMarkers;
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y ){

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

