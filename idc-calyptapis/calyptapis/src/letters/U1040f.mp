% U+1040F DESERET CAPITAL LETTER YEE (𐐏)
beginfig(1039);
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  path bar;
  bar := (x_radius, y_radius) -- (Ox, -y_radius);

  draw bar;

  pickup loz_pen;

  path serif;
  serif := ((2/3) * x_radius, y_radius)
          -- ((4/3) * x_radius, y_radius);
  draw serif;

  pickup thin_pen;
  path loop;
  loop := fullcircle scaled 0.75x_radius shifted (-1.25x_radius, 0.625y_radius);
  draw reverse loop cutafter point 2 of loop cutbefore point 6 of loop;

  pickup thin_pen;
  bar := (Ox, -y_radius)
         -- (-0.5x_radius, Oy){-((Ox,-y_radius)-(-0.5x_radius,Oy))}
         .. (point 2 of loop){left};
  draw bar;

  pickup thin_pen;
  path cross;
  cross := point 6 of loop
           .. point 6 of loop + (2x_radius, 0){right}
           .. tension 0.9
           .. point 6 of loop + (2.5x_radius, -0.25y_radius);
  draw cross cutafter point 1.75 of cross cutbefore point 0 of cross;

  pickup loz_pen rotated -45;
  draw cross cutafter point 2 of cross cutbefore point 1 of cross;

endfig;
