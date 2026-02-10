% ==============================================================================
% DTF Perdita - Base Parameters and Primitives
% ==============================================================================
% 
% DESIGN PHILOSOPHY:
% This font is based on the 1869 Oversize specimen, characterized by:
% - Strong vertical emphasis with slight calligraphic stress
% - Moderate stroke contrast (thick stems, thinner curves)
% - Compact proportions with generous counters
% - Ball terminals and organic curves
%
% ==============================================================================

% --- GLOBAL METRICS ---
% These define the font's overall proportions and rhythm

numeric font_size, em_square;
font_size  := 72pt;
em_square  := font_size;

% Vertical metrics (proportions of em-square)
numeric cap_height, x_height, descender_depth, ascender_height;
cap_height      := 0.7 * em_square;   % Capital letter height
x_height        := 0.5 * em_square;   % Lowercase x-height (for reference)
ascender_height := 0.75 * em_square;  % Tall letter height
descender_depth := 0.2 * em_square;   % Below baseline

% Horizontal metrics
numeric standard_width, narrow_width, wide_width;
standard_width := 0.6 * em_square;    % Typical letter width
narrow_width   := 0.4 * em_square;    % Narrow letters (I, l)
wide_width     := 0.8 * em_square;    % Wide letters (M, W)

% Stroke weights
numeric main_stem, thin_stroke, hairline;
main_stem   := 0.12 * em_square;      % Primary vertical/diagonal strokes
thin_stroke := 0.08 * em_square;      % Thinner curves/horizontals
hairline    := 0.04 * em_square;      % Finest details

% Serif dimensions
numeric serif_length, serif_height;
serif_length := 0.15 * em_square;     % Horizontal extent of serifs
serif_height := 0.08 * em_square;     % Vertical weight of serifs

% Curve parameters
numeric bowl_width, counter_ratio;
bowl_width    := 0.5 * em_square;     % Standard bowl/circle width
counter_ratio := 0.6;                 % Counter size relative to bowl (0-1)

% Reference point (origin for most glyphs)
numeric Ox, Oy;
Ox := 0;
Oy := 0;


% --- PEN DEFINITIONS ---
% Named pens for different stroke types

pen main_pen;     % Primary strokes
pen light_pen;    % Lighter strokes
pen serif_pen;    % Serif details
pen terminal_pen; % Rounded terminals (balls, teardrops)

main_pen     := pencircle scaled main_stem;
light_pen    := pencircle scaled thin_stroke;
serif_pen    := pensquare scaled serif_height;
terminal_pen := pencircle scaled (main_stem * 1.2);  % Slightly thicker for terminals


% --- GEOMETRIC PRIMITIVES ---
% Standard shapes and components for composition

% Standard circle (unit radius, centered at origin)
vardef standard_circle = 
  fullcircle scaled (2 * bowl_width)
enddef;

% Standard oval (vertical emphasis)
vardef standard_oval(expr aspect_ratio) =
  fullcircle xscaled bowl_width yscaled (bowl_width * aspect_ratio)
enddef;

% Arc from standard circle (start_angle to end_angle in degrees)
vardef arc(expr start_deg, end_deg, radius) =
  subpath (start_deg/45, end_deg/45) of (fullcircle scaled (2 * radius))
enddef;

% Spiral path (like '6' or '9' - grows as it curves)
% start_radius: initial radius
% end_radius: final radius
% turns: fraction of circle (0.75 = 3/4 circle)
vardef spiral_path(expr start_radius, end_radius, start_angle, turns) =
  save p, n, step_angle, current_radius;
  path p;
  numeric n, step_angle, current_radius;
  
  n := 20;  % Number of segments for smoothness
  step_angle := turns * 360 / n;
  
  p := (start_radius * cosd(start_angle), start_radius * sind(start_angle));
  
  for i = 1 upto n:
    current_radius := start_radius + (end_radius - start_radius) * (i/n);
    p := p .. (current_radius * cosd(start_angle + i * step_angle), 
               current_radius * sind(start_angle + i * step_angle));
  endfor;
  
  p
enddef;


% --- SERIF COMPONENTS ---
% Reusable serif builders

% Horizontal serif (like at top of 'I')
% pos: (x,y) position
% length: total horizontal extent
% side: -1 for left, 1 for right, 0 for centered
vardef horizontal_serif(expr pos, length, side) =
  save p;
  path p;
  
  if side = 0:  % Centered
    p := (xpart pos - length/2, ypart pos) -- (xpart pos + length/2, ypart pos);
  elseif side = -1:  % Extends left
    p := (xpart pos - length, ypart pos) -- (xpart pos, ypart pos);
  else:  % Extends right
    p := (xpart pos, ypart pos) -- (xpart pos + length, ypart pos);
  fi;
  
  p
enddef;

% Vertical serif
vardef vertical_serif(expr pos, height, side) =
  save p;
  path p;
  
  if side = 0:  % Centered
    p := (xpart pos, ypart pos - height/2) -- (xpart pos, ypart pos + height/2);
  elseif side = -1:  % Extends down
    p := (xpart pos, ypart pos - height) -- (xpart pos, ypart pos);
  else:  % Extends up
    p := (xpart pos, ypart pos) -- (xpart pos, ypart pos + height);
  fi;
  
  p
enddef;

% Ball terminal (rounded end of stroke)
vardef ball_terminal(expr pos, diameter) =
  fullcircle scaled diameter shifted pos
enddef;


% --- UTILITY MACROS ---

% Draw with variable-width pen (for organic curves)
% p: path to draw
% start_width, end_width: pen widths at start/end
% n_steps: smoothness (more = smoother)
vardef variable_width_draw(expr p, start_width, end_width, n_steps) =
  save i, t_start, t_end, current_width, plen;
  numeric i, t_start, t_end, current_width, plen;
  
  plen := length(p);
  
  for i = 0 upto n_steps - 1:
    t_start := (i / n_steps) * plen;
    t_end := ((i + 1) / n_steps) * plen;
    current_width := start_width + (end_width - start_width) * ((i + 0.5) / n_steps);
    
    pickup pencircle scaled current_width;
    draw subpath (t_start, t_end) of p;
  endfor;
enddef;


% --- OUTPUT CONFIGURATION ---

warningcheck := 0;
outputformat := "svg";
outputtemplate := "%j-%c.svg";

% Force integer RGB (avoid percentage warnings)
def rgbcolor(expr r, g, b) = 
  (r, g, b)
enddef;