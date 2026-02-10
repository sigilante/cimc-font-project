% U+1041B DESERET CAPITAL LETTER ETH (𐐛)
beginfig(1051);
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  path bar;
  bar := (Ox, -y_radius) -- (Ox, y_radius);

  draw bar;

  pickup loz_pen;
  path lower_serif;
  lower_serif := (-(1/3) * x_radius, -y_radius)
                 -- ((1/3) * x_radius, -y_radius);
  draw lower_serif;

  pickup loz_pen;
  path beam;
  beam := ((1/3) * x_radius, y_radius)
          -- (-(4/3) * x_radius, y_radius);
  draw beam;

  pickup loz_pen rotated -90;
  path serif;
  serif := (-(4/3)*x_radius+0.375*pen_height, y_radius){down}
          .. tension 0.9
          .. (-(4/3)*x_radius+0.375*pen_height, 0.75*y_radius-0.125*pen_height);
  draw serif;

  currentpicture := currentpicture rotated 180;

  draw currentpicture;
endfig;
