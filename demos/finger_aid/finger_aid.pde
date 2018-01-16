import java.io.*;
import java.util.concurrent.*;

String port = "COM6";
String modelPath = "C:\\Users\\Federico\\Documents\\finger_model.svm";
String scriptPath = "D:\\GitHub\\pygarl\\demos\\finger_aid.py";
DataThread dataThread = new DataThread();

Status status = Status.INIT;
String gesture = "make a gesture";

void setup() {
  size(1024, 768);
  orientation(LANDSCAPE);
   
  println("Starting DataThread...");
  dataThread.start();
} 

void draw () {
  background(0);
  
  String statusText = "STARTING...";
  
  if (status == Status.INIT) {
     statusText = "INITIALIZING...";
  }else if (status == Status.LOADING) {
     statusText = "LOADING..."; 
  }else if (status == Status.STARTED) {
     statusText = "STARTED";
  }
  
  
  textSize(16);
  text(statusText, width/2, 20); 
  
  textSize(64);
  textAlign(CENTER);
  text(gesture, width/2, height/2); 
}

public class DataThread extends Thread {  
  Process p;
  boolean shouldStop = false;
  
  public void run () {
    try {
      String line;
      println("Starting process...");
      ProcessBuilder pb = new ProcessBuilder("python", scriptPath, port, modelPath);
      pb.redirectErrorStream(true);
      p = pb.start();     
      
      BufferedReader input = new BufferedReader(new InputStreamReader(p.getInputStream()));
      
      while (!shouldStop && (line = input.readLine()) != null) {
        if (line.equals("LOADING")) {
          status = Status.LOADING;
        }else if (line.equals("LOADED")) {
          status = Status.LOADED; 
        }else if (line.equals("STARTED")) {
          status = Status.STARTED; 
        }else if (line.startsWith("GESTURE ")) {
          gesture = line.substring(8);
        }
        println(line);
        Thread.sleep(1);
      }
      
    } catch (Exception err) {
      err.printStackTrace();
    }
    println("Exiting...");
  }
  
  public void closePython() {
    p.destroyForcibly();
  }
}

void exit() {
  println("Closing...");
  dataThread.closePython();
  dataThread.shouldStop = true;
  super.exit();
}

enum Status {
  INIT,
  LOADING,
  LOADED,
  STARTED
}
 