% U+10407 DESERET CAPITAL LETTER SHORT E (𐐇)
beginfig(1031) ;
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

endfig;
