% U+10425 DESERET CAPITAL LETTER ENG (𐐥)
beginfig(1061) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  path bar;
  bar := (Ox, -y_radius) -- (Ox, y_radius);

  draw bar;
  draw bar shifted (1.5x_radius, 0);

  pickup loz_pen;

  path serif;
  serif := (-(1/3) * x_radius, y_radius)
          -- ((1/3) * x_radius, y_radius);
  draw serif;
  draw serif shifted (1.5x_radius, -2.0 * y_radius);

  path short;
  short := (1.5x_radius, y_radius)
           -- ((1/3) * x_radius+1.5x_radius, y_radius);
  draw short;

  pickup thin_pen;
  path beam;
  beam := point 0 of bar
          -- point 1 of bar shifted (1.5x_radius, 0);
  draw beam;

endfig;
