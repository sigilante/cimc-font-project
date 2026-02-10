% SVG output configuration
outputformat := "svg";
outputtemplate := "%j-%c.svg";

beginfig(1);

% ==== HIGH-LEVEL PARAMETERS ====
% These are the main controls for optimization

% Pen sizes
pen_thick := 13.212902;  % Thickest strokes
pen_thin := 12.194525;   % Thinnest strokes

% Curve tension (how tight the curves are)
global_tension := 1.107195;

% Overall scaling
x_scale := 0.970539;
y_scale := 0.784191;

% ==== BASE COORDINATES ====
% Individual point positions (before scaling)

% Segment 1 base coordinates
pen_ratio_start_a := 1.000;
pen_ratio_end_a := 1.000;

x_a_0_base := -12.571580;
y_a_0_base := 175.295856;
x_a_1_base := 86.590191;
y_a_1_base := -9.996384;
x_a_2_base := -11.981567;
y_a_2_base := -166.548286;
x_a_3_base := -124.110765;
y_a_3_base := -12.991101;
x_a_4_base := -14.869201;
y_a_4_base := 147.436051;

% Segment 2 base coordinates
pen_ratio_start_b := 1.000;
pen_ratio_end_b := 1.000;

x_b_0_base := -72.143907;
y_b_0_base := 138.333141;
x_b_1_base := 84.763961;
y_b_1_base := -29.868430;

% ==== DERIVED PARAMETERS ====
% Computed from high-level parameters

% Segment a scaled coordinates
x_a_0 := x_a_0_base * x_scale;
y_a_0 := y_a_0_base * y_scale;
x_a_1 := x_a_1_base * x_scale;
y_a_1 := y_a_1_base * y_scale;
x_a_2 := x_a_2_base * x_scale;
y_a_2 := y_a_2_base * y_scale;
x_a_3 := x_a_3_base * x_scale;
y_a_3 := y_a_3_base * y_scale;
x_a_4 := x_a_4_base * x_scale;
y_a_4 := y_a_4_base * y_scale;

% Segment b scaled coordinates
x_b_0 := x_b_0_base * x_scale;
y_b_0 := y_b_0_base * y_scale;
x_b_1 := x_b_1_base * x_scale;
y_b_1 := y_b_1_base * y_scale;

% Pen sizes (derived from ratios)
pen_start_a := pen_thick * pen_ratio_start_a;
pen_end_a := pen_thick * pen_ratio_end_a;
pen_start_b := pen_thick * pen_ratio_start_b;
pen_end_b := pen_thick * pen_ratio_end_b;

% ==== PATH DEFINITIONS ====

path seg_a;
seg_a := 
  (x_a_0, y_a_0){right}
  .. tension global_tension
  .. (x_a_1, y_a_1){down}
  .. tension global_tension
  .. (x_a_2, y_a_2){left}
  .. tension global_tension
  .. (x_a_3, y_a_3){up}
  .. tension global_tension
  .. (x_a_4, y_a_4){right}
  ;

path seg_b;
seg_b := 
  (x_b_0, y_b_0)
  .. tension global_tension
  .. (x_b_1, y_b_1){right}
  ;

% ==== DRAWING ====

n_seg := 20;

% Draw seg_a
pickup pencircle scaled pen_start_a;
draw seg_a;

% Draw seg_b
pickup pencircle scaled pen_start_b;
draw seg_b;

endfig;
end;