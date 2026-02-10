% U+1040A DESERET CAPITAL LETTER SHORT O (𐐊)
beginfig(1034) ;
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

  pickup loz_pen rotated 90;
  draw (-1.5*x_radius, -1.0*y_radius-0.375*pen_height)
       -- (-1.5*x_radius, -0.96*y_radius);

  pickup thin_pen;
  path arc;
  arc := halfcircle scaled (1.5*x_radius) shifted (-0.75*x_radius, -y_radius);

  draw arc cutbefore point 0 of arc cutafter point 3.925 of arc;

  currentpicture := currentpicture rotated 180;
  draw currentpicture;
endfig;
