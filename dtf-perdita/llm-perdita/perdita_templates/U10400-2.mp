input perdita_base.mp;

% ==============================================================================
% U+10400 DESERET CAPITAL LETTER LONG I (𐐀)
% ==============================================================================
%
% VISUAL DESCRIPTION:
% A horizontally-flipped '6' shape with a thick rectangular serif at top left.
% Main stroke has consistent width throughout.
%
% CONSTRUCTION:
% 1. Top rectangular terminal (serif/bar)
% 2. Descending curve from terminal, flowing down and right
% 3. Lower enclosed bowl (circular/oval)
%
% ==============================================================================

input perdita_base.mp;

beginfig(1024);
  
  % --- LOCAL PARAMETERS ---
  
  numeric bowl_diameter;      % Size of the lower circular bowl
  numeric bowl_center_x;      % Horizontal position of bowl center
  numeric bowl_center_y;      % Vertical position of bowl center
  
  numeric upper_curve_height; % How high the curve extends above bowl
  numeric upper_curve_x;      % Horizontal extent of upper curve
  
  numeric serif_width;        % Width of top rectangular terminal
  numeric serif_height;       % Height of top terminal
  numeric serif_x;            % X position of serif left edge
  numeric serif_y;            % Y position of serif top edge
  
  % Initial values (to be optimized)
  bowl_diameter := cap_height * 0.4763;
  bowl_center_x := bowl_diameter * 0.6329;
  bowl_center_y := bowl_diameter * 0.3837;
  
  upper_curve_height := cap_height * 0.7385;
  upper_curve_x := bowl_diameter * 0.1971;
  
  serif_width := bowl_diameter * 0.2972;
  serif_height := bowl_diameter * 0.1875;
  serif_x := -0.0990;
  serif_y := upper_curve_height;
  
  % --- CONSTRUCTION ---
  
  % Main stroke - composite path
  % Start at bottom of serif, curve down to bowl, complete bowl
  
  path main_stroke;
  
  % Lower bowl (complete circle)
  path lower_bowl;
  lower_bowl := fullcircle scaled bowl_diameter 
                shifted (bowl_center_x, bowl_center_y);
  
  % Upper connecting curve
  % From bottom of serif, curve down and connect to top of bowl
  path upper_curve;
  upper_curve := (serif_x + serif_width/2, serif_y - serif_height){down}
                 .. tension 1.2
                 .. (upper_curve_x, (upper_curve_height + bowl_center_y)/2){down}
                 .. tension 1.2
                 .. point 2 of lower_bowl;  % Top of bowl (12 o'clock position)
  
  % Draw main stroke
  pickup main_pen;
  draw upper_curve;
  draw lower_bowl;
  
  % Top rectangular serif/terminal
  pickup pensquare scaled serif_height;
  draw (serif_x, serif_y) -- (serif_x + serif_width, serif_y);
  
endfig;

end;
============================================================