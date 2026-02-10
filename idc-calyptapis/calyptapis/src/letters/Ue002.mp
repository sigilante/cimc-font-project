% U+E002 DESERET CAPITAL LETTER VARIANT SQUARE
beginfig(24578) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  path bar;
  bar := (Ox, -y_radius) -- (Ox, y_radius);

  draw bar;

  pickup loz_pen;

  path serif;
  serif := (-(1/3) * x_radius, y_radius)
          -- ((1/3) * x_radius, y_radius);
  draw serif;
  draw serif shifted (0, -2.0 * y_radius);
  draw serif shifted (-1.5*x_radius, -2.0 * y_radius);

  pickup thin_pen;
  path arc;
  arc := halfcircle scaled (1.5*x_radius) shifted (-0.75*x_radius, -y_radius);

  draw arc;

  pickup loz_pen rotated -15;
  path bar;
  bar := (-0.75*x_radius,-1.0*y_radius)
          .. tension 0.9
          .. (Ox,-1.0*y_radius-0.25*pen_height)
          .. tension 0.9
          .. (0.75*x_radius,-1.0*y_radius);
  draw bar rotatedaround ((Ox,-y_radius),-15)
           shifted (Ox-0.75*cosd(-15)*x_radius,Oy-0.75*sind(-15)*y_radius)
           shifted (0, y_radius);

endfig;
