% U+10418 DESERET CAPITAL LETTER GAY (𐐘)
beginfig(1048);
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  path lower_circle;
  lower_circle := (Ox, y_radius){left}
                .. tension 0.9
                .. (-x_radius, Oy){down}
                .. tension 0.9
                .. (Ox, -y_radius){right}
                .. tension 0.9
                .. (x_radius, Oy){up}
                .. tension 0.9
                .. cycle;

  lower_circle := lower_circle scaled (2/3) shifted (2/3*x_radius, -1/3*y_radius);
  draw subpath (1, 3) of lower_circle;
  draw subpath (1, 3) of lower_circle shifted ((4/3)*x_radius,0);

  pickup thin_pen;
  path bar;
  bar := (point 1 of lower_circle){up}
        .. tension 0.9
        .. (Ox, Oy)
        .. tension 0.9
        .. ((4/3)*x_radius, y_radius){right}
        .. tension 0.9
        .. ((8/3)*x_radius, Oy){down}
        .. tension 0.9
        .. ((point 1 of lower_circle) shifted ((8/3)*x_radius,0)){down};
  draw bar;

  pickup loz_pen;
  path serif;
  serif := (-(1/3) * x_radius, (-1/3)*y_radius)
  -- ((1/3) * x_radius, (-1/3)*y_radius);
  draw serif shifted ((4/3)*x_radius,0);

  pickup thin_pen;
  path loop;
  loop := (point 2 of bar){down}
          .. tension 0.9
          .. (point 2.875 of bar){right};
  draw loop;

  pickup loz_pen;
  path serif;
  serif := (point 2.875 of bar)
          -- (point 2.875 of bar)+((1/3)*x_radius,0);
  draw serif;

endfig;
