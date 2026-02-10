% U+10421 DESERET CAPITAL LETTER ER (𐐡)
beginfig(1057) ;
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

  pickup thin_pen;
  path swirl;
  swirl := (point 0.75 of bar){up}
          .. tension 0.9
          .. (-0.5x_radius, y_radius){left}
          .. tension 0.9
          .. (-x_radius, 0.5y_radius){down}
          .. tension 0.9
          .. (Ox, Oy){right}
          .. tension 0.9
          .. (0.75x_radius, 0.65y_radius){up}
          -- (0.75x_radius, y_radius);
  draw swirl shifted (0, -0.5y_radius);

  pickup loz_pen;
  draw serif shifted (0.75x_radius,-0.5y_radius);

endfig;
