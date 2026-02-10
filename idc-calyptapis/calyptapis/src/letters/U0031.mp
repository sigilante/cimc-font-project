% U+0031 DIGIT ONE (1)
beginfig(49) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  path bar;
  bar := (Ox, -y_radius) -- (Ox, y_radius);
  draw bar;

  % Flag at top-left
  path flag;
  flag := (Ox, y_radius)
          -- (-(1/3)*x_radius, (2/3)*y_radius);
  draw flag;

  pickup loz_pen;

  % Baseline serif
  path serif;
  serif := (-(1/3)*x_radius, -y_radius)
           -- ((1/3)*x_radius, -y_radius);
  draw serif;

  pickup loz_pen rotated 45;

  % Flag terminal tick
  path tick;
  tick := (-(1/3)*x_radius, (2/3)*y_radius)
          -- (-(1/3)*x_radius - 0.125*pen_height, (2/3)*y_radius - 0.125*pen_height);
  draw tick;

endfig;
