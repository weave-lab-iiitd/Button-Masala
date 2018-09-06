#include "ofMain.h"
#include "time.h"
class ofxTimer{

	bool bEnabled;
	bool start;
	int seconds;
	int minutes;
	int hours;
	int last_second;
	int time;
	ofRectangle rectButton;
 	int button_x;
	int button_y;
public:
	void setup(){
		start=false;
		bEnabled=true;
		seconds=0;
		minutes=0;
		hours=0;
		last_second=ofGetSeconds();
		time=0;
		button_x=700;
		button_y=50;
		rectButton.set(button_x, button_y, 100, 30);
	}

	void update(){
	  time=hours*3600+minutes*60+seconds;
	  if (time==0) {start=false;return ;}
	  if(start)
	  {	
		if(ofGetSeconds() != last_second)
		{
			time--;
			last_second=ofGetSeconds();			
	                hours=(int)time/3600.0;
	                minutes=(int)(time%3600)/60;
	                seconds=(int)time % 60;			
		}
       	  }	
	}
	
	void draw (){
	if(bEnabled)
	 {	
		if (start)
        		ofSetColor(ofColor::sandyBrown);
    		else
        		ofSetColor(ofColor::seaGreen);
		ofRect(rectButton);
		ofSetColor(ofColor::white);
		ofDrawBitmapString("START",button_x+10,button_y+20);
		ofDrawBitmapString(ofToString(hours)+" : "+ofToString(minutes)+": "+ofToString(seconds)+ ":"+ofToString(time),button_x-150,button_y+20);		
	 }		
	}
	void set_seconds(int s){seconds=s;}
	void set_minutes(int m){minutes=m;}
	void set_hours(int h){hours=h;}
	void set_bEnabled(){bEnabled=true;}
	void set_start(){start=true;last_second=ofGetSeconds();}
	int get_buttonx(){return button_x;}
	int get_buttony(){return button_y;}
};
