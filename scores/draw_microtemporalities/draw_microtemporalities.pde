import processing.pdf.*;
import org.philhosoft.p8g.svg.P8gGraphicsSVG;

import java.io.File;

Table table;

int horizontal_size = 2000;
int vertical_size = 1000;
float vscale = 500;
float hscale = 1;

int ms_increments = 100;

boolean done = false;

int max_width(Table table) {
  String[] ends = table.getStringColumn("End Time (ms)");
  return int(ends[ends.length -1]);
}

void setup()
{
  noLoop();      
  ellipseMode(CENTER);
  
  selectFolder("Select a folder to process:", "folderSelected");
}

void draw_info(int x, int y, String text) {
  
  fill(0);
  text(text, x, y);  
  
}

void draw_legend(int x, int y) {
  
  fill(0);
  text("Legend", x, y);
  
  int line_height = 20;
  
  y += line_height;
  noFill();
  text("ad\nanalytics\ntracker\nwidget\nprivacy\nother", x, y); 
  
  int width_line = 50;
  
  x += 60;
  
  // Ad
  y -= 4;
  stroke(0, 191, 243);
  line(x, y, x + width_line, y);
  fill(255);
  ellipse(x, y, 5, 5);
  ellipse(x + width_line, y, 5, 5);

  
  //Analytics
  y += 15;
  stroke(163, 170, 64);
  line(x, y , x + width_line, y);
  fill(255);
  ellipse(x, y, 5, 5);
  ellipse(x + width_line, y, 5, 5);
  
  //Tracker
  y += 14;
  stroke(208, 18, 49);
  line(x, y , x + width_line, y);
  fill(255);
  ellipse(x, y, 5, 5);
  ellipse(x + width_line, y, 5, 5);

  //Widget
  y += 13;
  stroke(0, 154, 138);
  line(x, y , x + width_line, y);
  fill(255);
  ellipse(x, y, 5, 5);
  ellipse(x + width_line, y, 5, 5);

  //Privacy
  y += 15;
  stroke(251, 88, 37);
  line(x, y , x + width_line, y);
  fill(255);
  ellipse(x, y, 5, 5);
  ellipse(x + width_line, y, 5, 5);
  
  //Other
  y += 15;
  stroke(0,0,0);
  line(x, y , x + width_line, y);
  fill(255);
  ellipse(x, y, 5, 5);
  ellipse(x + width_line, y, 5, 5);
  

}

void draw_graph(Table table, String input_file_name, String output_file_name) {
  
  TableRow first_row = table.getRow(0);
  String name_date_time = first_row.getString("Host") + "\n" + first_row.getString("Date") + "\n" + first_row.getString("Time") + " - CEST Amsterdam\n";
  String user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64)\nAppleWebKit/537.36 (KHTML, like Gecko)\nChrome/43.0.2357.132 Safari/537.36 PTST/221\n";
  
  String legend_text = name_date_time + "\n" + user_agent;
  
  println(name_date_time);
 
  horizontal_size = max_width(table) + 200;
  size(horizontal_size, vertical_size);

  beginRecord(P8gGraphicsSVG.SVG, output_file_name);
  
  draw_info(100, 100, legend_text);
  draw_legend(100, 225);
  
  int last = 0;
  float baseline = vertical_size/2;
  
  for (TableRow row : table.rows ()) {
    
    float start = row.getFloat("Start Time (ms)")/hscale;
    float end = row.getFloat("End Time (ms)")/hscale;
    float size = row.getFloat("Object Size")/vscale;
    String type = row.getString("bug_type");
    
    noFill();
    if(type.equals("analytics"))
    {
      stroke(163, 170, 64);
    } 
    else if(type.equals("ad"))
    {
      stroke(0, 191, 243);
    }
    else if(type.equals("tracker"))
    {
      stroke(208, 18, 49);
    }
    else if(type.equals("privacy"))
    {
      stroke(251, 88, 37);
    }    
    else if(type.equals("widget"))
    {
      stroke(0, 154, 138);
    }    
    else
    {
      stroke(0,0,0);
    }
    
    bezier(start, baseline, start + (end-start)/2, baseline, start + (end-start)/2, baseline + size, end, baseline + size);
    bezier(start, baseline, start + (end-start)/2, baseline, start + (end-start)/2, baseline - size, end, baseline - size);
    
    fill(255);
    ellipse(start, baseline, 5, 5);
    ellipse(end, baseline + size, 5, 5);
    ellipse(end, baseline - size, 5, 5);
    
    last = (int)end;
  }
  
  fill(0);
  int nbr_tick = (last / ms_increments) + 1;
  for(int i = 1; i < nbr_tick; i++) {
    String t = (i * ms_increments) + " ms";
    text(t, i * ms_increments, baseline + 50); 
  } 
  
  endRecord(); 
}

void draw()
{  
  if (!done)
    background(255,0,0);
  else
    background(255,255,255);
    
}

void folderSelected(File dir) {
  if (dir != null) {
    File[] files = dir.listFiles();
    for (int i = 0; i < files.length; i++) {
      process(files[i]);
    }
  }  
  done = true;
}

void process(File file) {
   String input_file_name = file.getName();
   String output_file_name = input_file_name + ".svg";
   
   if(input_file_name.endsWith(".csv")) {
     println(input_file_name);
     Table table = loadTable(file.getPath(), "header");  
     draw_graph(table, input_file_name, output_file_name);
     println("done");
   }
   
}

