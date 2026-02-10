% U+003B SEMICOLON (;)
beginfig(59) ;
  pickup thin_pen;
  drawdot (Ox, (1/3)*y_radius);
  drawdot (Ox, -y_radius);

  pickup loz_pen;
  path tail;
  tail := (Ox, -y_radius){down}
          .. tension 0.9
          .. (-(1/6)*x_radius, -y_radius - (1/3)*y_radius);
  draw tail;
endfig;
