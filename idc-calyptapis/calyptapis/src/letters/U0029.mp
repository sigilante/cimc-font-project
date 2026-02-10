% U+0029 RIGHT PARENTHESIS ())
beginfig(41) ;
  pickup thin_pen;
  path rparen;
  rparen := (-(1/3)*x_radius, y_radius){right}
            .. tension 0.9
            .. ((1/3)*x_radius, Oy){down}
            .. tension 0.9
            .. (-(1/3)*x_radius, -y_radius){left};
  draw rparen;
endfig;
