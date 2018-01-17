import java.io.*;
import java.util.concurrent.*;

String port = "COM6";
String modelPath = "D:\\GitHub\\pygarl\\demos\\model.svm";
String scriptPath = "D:\\GitHub\\pygarl\\demos\\finger_aid.py";
DataThread dataThread = new DataThread();

Status status = Status.INIT;
String gesture = "make a gesture";
int alpha = 255;
float alphaSpeed = 5;

String currentText = "";

int rowCount = 3;
int colCount = 3;

int row = 1;
int col = 1;
int page = 0;

int rowSize;
int colSize;

char[] letters = "abcdefghijklmnopqrstuvwxyz".toCharArray();

void setup() {
  size(1024, 768);
  orientation(LANDSCAPE);
   
  println("Starting DataThread...");
  dataThread.start();
  
  rowSize = height/rowCount;
  colSize = width/colCount;

} 

void draw () {
  background(0);
  
  for (int r = 0; r < rowCount; r++) {
     for (int c = 0; c < colCount; c++) {
         if (r == row && c == col) {
            fill(0,0,100, 150); 
         }else{
            fill(30,30,30, 255); 
         }
         rect(c*colSize, r*rowSize, colSize, rowSize);
         
         fill(255, 255, 255);
         int index = (page*colCount*rowCount) + c + r*colCount;
         if (index < letters.length) {
           textSize(64);
           text(letters[index], c*colSize+colSize/2, r*rowSize+rowSize/2); 
         }
     }
  }
  
  String statusText = "STARTING...";
  
  fill(255,255,255);
  if (status == Status.INIT) {
     statusText = "INITIALIZING...";
  }else if (status == Status.LOADING) {
     statusText = "LOADING..."; 
  }else if (status == Status.STARTED) {
     statusText = "STARTED";
     fill(0, 255, 0, 255);
  }else if (status == Status.ERROR) {
     statusText = "ERROR";
     fill(255, 0, 0, 255);
  }
  
  
  textSize(16);
  text(statusText, width/2, 20); 
  
  textSize(32);
  textAlign(CENTER);
  fill(255,255,255, 255);
  text("\""+currentText+"\"", width/2, 50);
  
  textSize(32);
  textAlign(CENTER);
  fill(255,255,255, alpha);
  text(gesture, width/2, height/2);
  
  alpha-=alphaSpeed;
}

void receiveGesture(String g) {
  gesture = g;
  alpha = 255;
  if (g.equals("left")) {
    if (col > 0) {
      col--;
    }else{
      col = colCount-1; 
    }
  }else if (g.equals("right")) {
    if ((col+1) < colCount) {
      col++;
    }else{
      col = 0; 
    }
  }else if (g.equals("pull")) {
    if ((row+1) < rowCount) {
      row++;
    }else{
      row = 0; 
    }
  }else if (g.equals("push")) {
    if (row > 0) {
      row--;
    }else{
      row = rowCount-1; 
    }
  }else if (g.equals("doubletap")) {
    int numPages = ((int)(letters.length /(colCount*rowCount)))+1;
    if ((page+1) < numPages) {
      page++;
    }else{
      page=0;
    }
  }else if (g.equals("tapclockwise")) {
    currentText += " ";
  }else if (g.equals("tapanticlockwise")) {
    if (currentText.length()>0) {
      currentText = currentText.substring(0, currentText.length()-1); 
    }
  }else if (g.equals("tap")) {
     int index = (page*colCount*rowCount) + col + row*colCount;
     if (index < letters.length) {
       currentText += letters[index];
     }
  }
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
        }else if (line.equals("EXCEPTION")) {
          status = Status.ERROR; 
        }else if (line.startsWith("GESTURE ")) {
          receiveGesture(line.substring(8));
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
  STARTED,
  ERROR
}
 