% SVG output configuration
outputformat := "svg";
outputtemplate := "%j-%c.svg";

beginfig(1);

% Segment 1
path seg_a;
seg_a := 
  (-12.0, 163.0){right}
  .. tension 1.00
  .. (88.0, -10.0){down}
  .. tension 1.00
  .. (-12.0, -179.0){left}
  .. tension 1.00
  .. (-117.0, -13.0){up}
  .. tension 1.00
  .. (-14.0, 163.0){right}
  ;

% Segment 2
path seg_b;
seg_b := 
  (-71.0, 138.0)
  .. tension 1.00
  .. (89.0, -29.0){right}
  ;

% Drawing variables
numeric n_seg, plen, i, t_start, t_end, current_pen;
n_seg := 20;

% Draw seg_a
pickup pencircle scaled 12.0;
draw seg_a;

% Draw seg_b
pickup pencircle scaled 12.0;
draw seg_b;

endfig;
end;