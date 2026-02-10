% U+10406 DESERET CAPITAL LETTER SHORT I (𐐆)
beginfig(1030) ;
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

  pickup loz_pen rotated -15;
  path beam;
  beam := (-0.5 * x_radius, Oy)
          -- (0.5 * x_radius, Oy);
  draw beam rotated -15;

endfig;
