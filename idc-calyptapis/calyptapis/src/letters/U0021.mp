% U+0021 EXCLAMATION MARK (!)
beginfig(33) ;
  pickup thin_pen;
  path stroke;
  stroke := (Ox, y_radius)
            -- (Ox, -(1/3)*y_radius);
  draw stroke;

  drawdot (Ox, -(5/6)*y_radius);
endfig;
