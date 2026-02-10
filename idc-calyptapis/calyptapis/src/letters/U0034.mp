% U+0034 DIGIT FOUR (4)
beginfig(52) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  % Vertical stroke on the right
  path bar;
  bar := ((1/3)*x_radius, -y_radius) -- ((1/3)*x_radius, y_radius);
  draw bar;

  % Diagonal from crossbar at left up to top of vertical
  path diagonal;
  diagonal := (-x_radius, -(1/6)*y_radius)
              -- ((1/3)*x_radius, y_radius);
  draw diagonal;

  % Horizontal crossbar
  path crossbar;
  crossbar := (-x_radius, -(1/6)*y_radius)
              -- ((2/3)*x_radius, -(1/6)*y_radius);
  draw crossbar;

  pickup loz_pen;

  % Baseline serif
  path serif;
  serif := (-(1/3)*x_radius+(1/3)*x_radius, -y_radius)
           -- ((1/3)*x_radius+(1/3)*x_radius, -y_radius);
  draw serif;

endfig;
