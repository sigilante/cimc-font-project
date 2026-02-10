% U+0032 DIGIT TWO (2)
beginfig(50) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  % Upper arch
  path upper_circle;
  path lower_arc;
  upper_circle := (-x_radius, (1/2)*y_radius){up}
                  .. tension 0.9
                  .. (Ox, y_radius){right}
                  .. tension 0.9
                  .. (x_radius, Oy){down};
  upper_circle := upper_circle scaled (2/3) shifted (0*x_radius, 1/3*y_radius);
  draw upper_circle;

  % Diagonal descent from right end of arch to left end of baseline
  path diagonal;
  diagonal := ((2/3)*x_radius, (1/3)*y_radius){down}
              .. tension 0.9
              .. (-(2/3)*x_radius, -y_radius){down};
  draw diagonal;

  % Baseline bar
  path baseline;
  pickup loz_pen;
  baseline := (-(2/3)*x_radius-0.375*pen_height, -y_radius)
              -- ((2/3)*x_radius, -y_radius);
  draw baseline;

  % Serif at lower right
  pickup loz_pen rotated 90;
  path serif;
  serif := ((2/3)*x_radius, -y_radius-0.375*pen_height)
           -- ((2/3)*x_radius, -y_radius+0.125*pen_height+ (1/3)*y_radius);
  draw serif;

endfig;
