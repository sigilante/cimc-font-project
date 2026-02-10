% U+10424 DESERET CAPITAL LETTER EN (𐐤)
beginfig(1060) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup loz_pen;
  path serif;
  serif := (-(1/3) * x_radius, y_radius)
          -- ((1/3) * x_radius, y_radius);
  draw serif shifted (-(1/3)*x_radius,0);
  draw serif shifted ((1/3)*x_radius, -2.0 * y_radius);

  pickup loz_pen rotated 15;
  path beam;
  beam := ((1/3) * x_radius, Oy)
          -- (-(1/3) * x_radius, Oy);
  beam := beam rotated 15;
  draw beam;

  pickup thin_pen;
  path bar;
  bar := (-(1/3) * x_radius, y_radius) -- (-(1/3) * x_radius * cosd(15), (-1/3)*y_radius * sind(15));
  draw bar;
  bar := ((1/3) * x_radius * cosd(15), (1/3)*y_radius * sind(15)) -- ((1/3) * x_radius, -y_radius);
  draw bar;

endfig;
