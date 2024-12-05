var Fa = Object.defineProperty;
var Qi = (l) => {
  throw TypeError(l);
};
var za = (l, e, t) => e in l ? Fa(l, e, { enumerable: !0, configurable: !0, writable: !0, value: t }) : l[e] = t;
var Ce = (l, e, t) => za(l, typeof e != "symbol" ? e + "" : e, t), xi = (l, e, t) => e.has(l) || Qi("Cannot " + t);
var Ht = (l, e, t) => (xi(l, e, "read from private field"), t ? t.call(l) : e.get(l)), $i = (l, e, t) => e.has(l) ? Qi("Cannot add the same private member more than once") : e instanceof WeakSet ? e.add(l) : e.set(l, t), eo = (l, e, t, n) => (xi(l, e, "write to private field"), n ? n.call(l, t) : e.set(l, t), t);
const {
  SvelteComponent: Ba,
  assign: qa,
  children: ja,
  claim_element: Ha,
  create_slot: Va,
  detach: to,
  element: Wa,
  get_all_dirty_from_scope: Ga,
  get_slot_changes: Ya,
  get_spread_update: Xa,
  init: Za,
  insert_hydration: Ka,
  safe_not_equal: Ja,
  set_dynamic_element_data: no,
  set_style: ve,
  toggle_class: Qe,
  transition_in: Pr,
  transition_out: Ur,
  update_slot_base: Qa
} = window.__gradio__svelte__internal;
function xa(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), o = Va(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let s = [{
    "data-testid": (
      /*test_id*/
      l[7]
    )
  }, {
    id: (
      /*elem_id*/
      l[2]
    )
  }, {
    class: t = "block " + /*elem_classes*/
    l[3].join(" ") + " svelte-nl1om8"
  }], f = {};
  for (let a = 0; a < s.length; a += 1)
    f = qa(f, s[a]);
  return {
    c() {
      e = Wa(
        /*tag*/
        l[14]
      ), o && o.c(), this.h();
    },
    l(a) {
      e = Ha(
        a,
        /*tag*/
        (l[14] || "null").toUpperCase(),
        {
          "data-testid": !0,
          id: !0,
          class: !0
        }
      );
      var r = ja(e);
      o && o.l(r), r.forEach(to), this.h();
    },
    h() {
      no(
        /*tag*/
        l[14]
      )(e, f), Qe(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), Qe(
        e,
        "padded",
        /*padding*/
        l[6]
      ), Qe(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), Qe(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), Qe(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), ve(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), ve(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), ve(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), ve(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), ve(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), ve(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), ve(e, "border-width", "var(--block-border-width)");
    },
    m(a, r) {
      Ka(a, e, r), o && o.m(e, null), n = !0;
    },
    p(a, r) {
      o && o.p && (!n || r & /*$$scope*/
      131072) && Qa(
        o,
        i,
        a,
        /*$$scope*/
        a[17],
        n ? Ya(
          i,
          /*$$scope*/
          a[17],
          r,
          null
        ) : Ga(
          /*$$scope*/
          a[17]
        ),
        null
      ), no(
        /*tag*/
        a[14]
      )(e, f = Xa(s, [(!n || r & /*test_id*/
      128) && {
        "data-testid": (
          /*test_id*/
          a[7]
        )
      }, (!n || r & /*elem_id*/
      4) && {
        id: (
          /*elem_id*/
          a[2]
        )
      }, (!n || r & /*elem_classes*/
      8 && t !== (t = "block " + /*elem_classes*/
      a[3].join(" ") + " svelte-nl1om8")) && {
        class: t
      }])), Qe(
        e,
        "hidden",
        /*visible*/
        a[10] === !1
      ), Qe(
        e,
        "padded",
        /*padding*/
        a[6]
      ), Qe(
        e,
        "border_focus",
        /*border_mode*/
        a[5] === "focus"
      ), Qe(
        e,
        "border_contrast",
        /*border_mode*/
        a[5] === "contrast"
      ), Qe(e, "hide-container", !/*explicit_call*/
      a[8] && !/*container*/
      a[9]), r & /*height*/
      1 && ve(
        e,
        "height",
        /*get_dimension*/
        a[15](
          /*height*/
          a[0]
        )
      ), r & /*width*/
      2 && ve(e, "width", typeof /*width*/
      a[1] == "number" ? `calc(min(${/*width*/
      a[1]}px, 100%))` : (
        /*get_dimension*/
        a[15](
          /*width*/
          a[1]
        )
      )), r & /*variant*/
      16 && ve(
        e,
        "border-style",
        /*variant*/
        a[4]
      ), r & /*allow_overflow*/
      2048 && ve(
        e,
        "overflow",
        /*allow_overflow*/
        a[11] ? "visible" : "hidden"
      ), r & /*scale*/
      4096 && ve(
        e,
        "flex-grow",
        /*scale*/
        a[12]
      ), r & /*min_width*/
      8192 && ve(e, "min-width", `calc(min(${/*min_width*/
      a[13]}px, 100%))`);
    },
    i(a) {
      n || (Pr(o, a), n = !0);
    },
    o(a) {
      Ur(o, a), n = !1;
    },
    d(a) {
      a && to(e), o && o.d(a);
    }
  };
}
function $a(l) {
  let e, t = (
    /*tag*/
    l[14] && xa(l)
  );
  return {
    c() {
      t && t.c();
    },
    l(n) {
      t && t.l(n);
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (Pr(t, n), e = !0);
    },
    o(n) {
      Ur(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function es(l, e, t) {
  let {
    $$slots: n = {},
    $$scope: i
  } = e, {
    height: o = void 0
  } = e, {
    width: s = void 0
  } = e, {
    elem_id: f = ""
  } = e, {
    elem_classes: a = []
  } = e, {
    variant: r = "solid"
  } = e, {
    border_mode: c = "base"
  } = e, {
    padding: u = !0
  } = e, {
    type: _ = "normal"
  } = e, {
    test_id: m = void 0
  } = e, {
    explicit_call: p = !1
  } = e, {
    container: y = !0
  } = e, {
    visible: C = !0
  } = e, {
    allow_overflow: E = !0
  } = e, {
    scale: b = null
  } = e, {
    min_width: v = 0
  } = e, g = _ === "fieldset" ? "fieldset" : "div";
  const S = (w) => {
    if (w !== void 0) {
      if (typeof w == "number")
        return w + "px";
      if (typeof w == "string")
        return w;
    }
  };
  return l.$$set = (w) => {
    "height" in w && t(0, o = w.height), "width" in w && t(1, s = w.width), "elem_id" in w && t(2, f = w.elem_id), "elem_classes" in w && t(3, a = w.elem_classes), "variant" in w && t(4, r = w.variant), "border_mode" in w && t(5, c = w.border_mode), "padding" in w && t(6, u = w.padding), "type" in w && t(16, _ = w.type), "test_id" in w && t(7, m = w.test_id), "explicit_call" in w && t(8, p = w.explicit_call), "container" in w && t(9, y = w.container), "visible" in w && t(10, C = w.visible), "allow_overflow" in w && t(11, E = w.allow_overflow), "scale" in w && t(12, b = w.scale), "min_width" in w && t(13, v = w.min_width), "$$scope" in w && t(17, i = w.$$scope);
  }, [o, s, f, a, r, c, u, m, p, y, C, E, b, v, g, S, _, i, n];
}
class ts extends Ba {
  constructor(e) {
    super(), Za(this, e, es, $a, Ja, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: ns,
  append_hydration: Al,
  attr: Fn,
  children: lo,
  claim_component: ls,
  claim_element: io,
  claim_space: is,
  claim_text: os,
  create_component: rs,
  destroy_component: as,
  detach: Sl,
  element: oo,
  init: ss,
  insert_hydration: fs,
  mount_component: cs,
  safe_not_equal: us,
  set_data: _s,
  space: ds,
  text: ms,
  toggle_class: Et,
  transition_in: hs,
  transition_out: gs
} = window.__gradio__svelte__internal;
function bs(l) {
  let e, t, n, i, o, s;
  return n = new /*Icon*/
  l[1]({}), {
    c() {
      e = oo("label"), t = oo("span"), rs(n.$$.fragment), i = ds(), o = ms(
        /*label*/
        l[0]
      ), this.h();
    },
    l(f) {
      e = io(f, "LABEL", {
        for: !0,
        "data-testid": !0,
        class: !0
      });
      var a = lo(e);
      t = io(a, "SPAN", {
        class: !0
      });
      var r = lo(t);
      ls(n.$$.fragment, r), r.forEach(Sl), i = is(a), o = os(
        a,
        /*label*/
        l[0]
      ), a.forEach(Sl), this.h();
    },
    h() {
      Fn(t, "class", "svelte-9gxdi0"), Fn(e, "for", ""), Fn(e, "data-testid", "block-label"), Fn(e, "class", "svelte-9gxdi0"), Et(e, "hide", !/*show_label*/
      l[2]), Et(e, "sr-only", !/*show_label*/
      l[2]), Et(
        e,
        "float",
        /*float*/
        l[4]
      ), Et(
        e,
        "hide-label",
        /*disable*/
        l[3]
      );
    },
    m(f, a) {
      fs(f, e, a), Al(e, t), cs(n, t, null), Al(e, i), Al(e, o), s = !0;
    },
    p(f, [a]) {
      (!s || a & /*label*/
      1) && _s(
        o,
        /*label*/
        f[0]
      ), (!s || a & /*show_label*/
      4) && Et(e, "hide", !/*show_label*/
      f[2]), (!s || a & /*show_label*/
      4) && Et(e, "sr-only", !/*show_label*/
      f[2]), (!s || a & /*float*/
      16) && Et(
        e,
        "float",
        /*float*/
        f[4]
      ), (!s || a & /*disable*/
      8) && Et(
        e,
        "hide-label",
        /*disable*/
        f[3]
      );
    },
    i(f) {
      s || (hs(n.$$.fragment, f), s = !0);
    },
    o(f) {
      gs(n.$$.fragment, f), s = !1;
    },
    d(f) {
      f && Sl(e), as(n);
    }
  };
}
function ps(l, e, t) {
  let {
    label: n = null
  } = e, {
    Icon: i
  } = e, {
    show_label: o = !0
  } = e, {
    disable: s = !1
  } = e, {
    float: f = !0
  } = e;
  return l.$$set = (a) => {
    "label" in a && t(0, n = a.label), "Icon" in a && t(1, i = a.Icon), "show_label" in a && t(2, o = a.show_label), "disable" in a && t(3, s = a.disable), "float" in a && t(4, f = a.float);
  }, [n, i, o, s, f];
}
class ws extends ns {
  constructor(e) {
    super(), ss(this, e, ps, bs, us, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: ks,
  append_hydration: ui,
  attr: ut,
  bubble: vs,
  children: _i,
  claim_component: Es,
  claim_element: di,
  claim_space: ys,
  claim_text: Ts,
  create_component: As,
  destroy_component: Ss,
  detach: wn,
  element: mi,
  init: Cs,
  insert_hydration: Fr,
  listen: Ls,
  mount_component: Is,
  safe_not_equal: Rs,
  set_data: Ds,
  set_style: Vt,
  space: Ns,
  text: Os,
  toggle_class: ge,
  transition_in: Ms,
  transition_out: Ps
} = window.__gradio__svelte__internal;
function ro(l) {
  let e, t;
  return {
    c() {
      e = mi("span"), t = Os(
        /*label*/
        l[1]
      ), this.h();
    },
    l(n) {
      e = di(n, "SPAN", {
        class: !0
      });
      var i = _i(e);
      t = Ts(
        i,
        /*label*/
        l[1]
      ), i.forEach(wn), this.h();
    },
    h() {
      ut(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      Fr(n, e, i), ui(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && Ds(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && wn(e);
    }
  };
}
function Us(l) {
  let e, t, n, i, o, s, f, a = (
    /*show_label*/
    l[2] && ro(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = mi("button"), a && a.c(), t = Ns(), n = mi("div"), As(i.$$.fragment), this.h();
    },
    l(r) {
      e = di(r, "BUTTON", {
        "aria-label": !0,
        "aria-haspopup": !0,
        title: !0,
        class: !0
      });
      var c = _i(e);
      a && a.l(c), t = ys(c), n = di(c, "DIV", {
        class: !0
      });
      var u = _i(n);
      Es(i.$$.fragment, u), u.forEach(wn), c.forEach(wn), this.h();
    },
    h() {
      ut(n, "class", "svelte-1lrphxw"), ge(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), ge(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), ge(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], ut(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), ut(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), ut(
        e,
        "title",
        /*label*/
        l[1]
      ), ut(e, "class", "svelte-1lrphxw"), ge(
        e,
        "pending",
        /*pending*/
        l[3]
      ), ge(
        e,
        "padded",
        /*padded*/
        l[5]
      ), ge(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), ge(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), Vt(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), Vt(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), Vt(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(r, c) {
      Fr(r, e, c), a && a.m(e, null), ui(e, t), ui(e, n), Is(i, n, null), o = !0, s || (f = Ls(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), s = !0);
    },
    p(r, [c]) {
      /*show_label*/
      r[2] ? a ? a.p(r, c) : (a = ro(r), a.c(), a.m(e, t)) : a && (a.d(1), a = null), (!o || c & /*size*/
      16) && ge(
        n,
        "small",
        /*size*/
        r[4] === "small"
      ), (!o || c & /*size*/
      16) && ge(
        n,
        "large",
        /*size*/
        r[4] === "large"
      ), (!o || c & /*size*/
      16) && ge(
        n,
        "medium",
        /*size*/
        r[4] === "medium"
      ), (!o || c & /*disabled*/
      128) && (e.disabled = /*disabled*/
      r[7]), (!o || c & /*label*/
      2) && ut(
        e,
        "aria-label",
        /*label*/
        r[1]
      ), (!o || c & /*hasPopup*/
      256) && ut(
        e,
        "aria-haspopup",
        /*hasPopup*/
        r[8]
      ), (!o || c & /*label*/
      2) && ut(
        e,
        "title",
        /*label*/
        r[1]
      ), (!o || c & /*pending*/
      8) && ge(
        e,
        "pending",
        /*pending*/
        r[3]
      ), (!o || c & /*padded*/
      32) && ge(
        e,
        "padded",
        /*padded*/
        r[5]
      ), (!o || c & /*highlight*/
      64) && ge(
        e,
        "highlight",
        /*highlight*/
        r[6]
      ), (!o || c & /*transparent*/
      512) && ge(
        e,
        "transparent",
        /*transparent*/
        r[9]
      ), c & /*disabled, _color*/
      4224 && Vt(e, "color", !/*disabled*/
      r[7] && /*_color*/
      r[12] ? (
        /*_color*/
        r[12]
      ) : "var(--block-label-text-color)"), c & /*disabled, background*/
      1152 && Vt(e, "--bg-color", /*disabled*/
      r[7] ? "auto" : (
        /*background*/
        r[10]
      )), c & /*offset*/
      2048 && Vt(
        e,
        "margin-left",
        /*offset*/
        r[11] + "px"
      );
    },
    i(r) {
      o || (Ms(i.$$.fragment, r), o = !0);
    },
    o(r) {
      Ps(i.$$.fragment, r), o = !1;
    },
    d(r) {
      r && wn(e), a && a.d(), Ss(i), s = !1, f();
    }
  };
}
function Fs(l, e, t) {
  let n, {
    Icon: i
  } = e, {
    label: o = ""
  } = e, {
    show_label: s = !1
  } = e, {
    pending: f = !1
  } = e, {
    size: a = "small"
  } = e, {
    padded: r = !0
  } = e, {
    highlight: c = !1
  } = e, {
    disabled: u = !1
  } = e, {
    hasPopup: _ = !1
  } = e, {
    color: m = "var(--block-label-text-color)"
  } = e, {
    transparent: p = !1
  } = e, {
    background: y = "var(--background-fill-primary)"
  } = e, {
    offset: C = 0
  } = e;
  function E(b) {
    vs.call(this, l, b);
  }
  return l.$$set = (b) => {
    "Icon" in b && t(0, i = b.Icon), "label" in b && t(1, o = b.label), "show_label" in b && t(2, s = b.show_label), "pending" in b && t(3, f = b.pending), "size" in b && t(4, a = b.size), "padded" in b && t(5, r = b.padded), "highlight" in b && t(6, c = b.highlight), "disabled" in b && t(7, u = b.disabled), "hasPopup" in b && t(8, _ = b.hasPopup), "color" in b && t(13, m = b.color), "transparent" in b && t(9, p = b.transparent), "background" in b && t(10, y = b.background), "offset" in b && t(11, C = b.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = c ? "var(--color-accent)" : m);
  }, [i, o, s, f, a, r, c, u, _, p, y, C, n, m, E];
}
let St = class extends ks {
  constructor(e) {
    super(), Cs(this, e, Fs, Us, Rs, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
};
const {
  SvelteComponent: zs,
  append_hydration: Bs,
  attr: Cl,
  binding_callbacks: qs,
  children: ao,
  claim_element: so,
  create_slot: js,
  detach: Ll,
  element: fo,
  get_all_dirty_from_scope: Hs,
  get_slot_changes: Vs,
  init: Ws,
  insert_hydration: Gs,
  safe_not_equal: Ys,
  toggle_class: yt,
  transition_in: Xs,
  transition_out: Zs,
  update_slot_base: Ks
} = window.__gradio__svelte__internal;
function Js(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[5].default
  ), o = js(
    i,
    l,
    /*$$scope*/
    l[4],
    null
  );
  return {
    c() {
      e = fo("div"), t = fo("div"), o && o.c(), this.h();
    },
    l(s) {
      e = so(s, "DIV", {
        class: !0,
        "aria-label": !0
      });
      var f = ao(e);
      t = so(f, "DIV", {
        class: !0
      });
      var a = ao(t);
      o && o.l(a), a.forEach(Ll), f.forEach(Ll), this.h();
    },
    h() {
      Cl(t, "class", "icon svelte-3w3rth"), Cl(e, "class", "empty svelte-3w3rth"), Cl(e, "aria-label", "Empty value"), yt(
        e,
        "small",
        /*size*/
        l[0] === "small"
      ), yt(
        e,
        "large",
        /*size*/
        l[0] === "large"
      ), yt(
        e,
        "unpadded_box",
        /*unpadded_box*/
        l[1]
      ), yt(
        e,
        "small_parent",
        /*parent_height*/
        l[3]
      );
    },
    m(s, f) {
      Gs(s, e, f), Bs(e, t), o && o.m(t, null), l[6](e), n = !0;
    },
    p(s, [f]) {
      o && o.p && (!n || f & /*$$scope*/
      16) && Ks(
        o,
        i,
        s,
        /*$$scope*/
        s[4],
        n ? Vs(
          i,
          /*$$scope*/
          s[4],
          f,
          null
        ) : Hs(
          /*$$scope*/
          s[4]
        ),
        null
      ), (!n || f & /*size*/
      1) && yt(
        e,
        "small",
        /*size*/
        s[0] === "small"
      ), (!n || f & /*size*/
      1) && yt(
        e,
        "large",
        /*size*/
        s[0] === "large"
      ), (!n || f & /*unpadded_box*/
      2) && yt(
        e,
        "unpadded_box",
        /*unpadded_box*/
        s[1]
      ), (!n || f & /*parent_height*/
      8) && yt(
        e,
        "small_parent",
        /*parent_height*/
        s[3]
      );
    },
    i(s) {
      n || (Xs(o, s), n = !0);
    },
    o(s) {
      Zs(o, s), n = !1;
    },
    d(s) {
      s && Ll(e), o && o.d(s), l[6](null);
    }
  };
}
function Qs(l, e, t) {
  let n, {
    $$slots: i = {},
    $$scope: o
  } = e, {
    size: s = "small"
  } = e, {
    unpadded_box: f = !1
  } = e, a;
  function r(u) {
    var p;
    if (!u) return !1;
    const {
      height: _
    } = u.getBoundingClientRect(), {
      height: m
    } = ((p = u.parentElement) == null ? void 0 : p.getBoundingClientRect()) || {
      height: _
    };
    return _ > m + 2;
  }
  function c(u) {
    qs[u ? "unshift" : "push"](() => {
      a = u, t(2, a);
    });
  }
  return l.$$set = (u) => {
    "size" in u && t(0, s = u.size), "unpadded_box" in u && t(1, f = u.unpadded_box), "$$scope" in u && t(4, o = u.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty & /*el*/
    4 && t(3, n = r(a));
  }, [s, f, a, n, o, i, c];
}
class xs extends zs {
  constructor(e) {
    super(), Ws(this, e, Qs, Js, Ys, {
      size: 0,
      unpadded_box: 1
    });
  }
}
const {
  SvelteComponent: $s,
  append_hydration: Il,
  attr: Fe,
  children: zn,
  claim_svg_element: Bn,
  detach: cn,
  init: ef,
  insert_hydration: tf,
  noop: Rl,
  safe_not_equal: nf,
  set_style: xe,
  svg_element: qn
} = window.__gradio__svelte__internal;
function lf(l) {
  let e, t, n, i;
  return {
    c() {
      e = qn("svg"), t = qn("g"), n = qn("path"), i = qn("path"), this.h();
    },
    l(o) {
      e = Bn(o, "svg", {
        width: !0,
        height: !0,
        viewBox: !0,
        version: !0,
        xmlns: !0,
        "xmlns:xlink": !0,
        "xml:space": !0,
        stroke: !0,
        style: !0
      });
      var s = zn(e);
      t = Bn(s, "g", {
        transform: !0
      });
      var f = zn(t);
      n = Bn(f, "path", {
        d: !0,
        style: !0
      }), zn(n).forEach(cn), f.forEach(cn), i = Bn(s, "path", {
        d: !0,
        style: !0
      }), zn(i).forEach(cn), s.forEach(cn), this.h();
    },
    h() {
      Fe(n, "d", "M18,6L6.087,17.913"), xe(n, "fill", "none"), xe(n, "fill-rule", "nonzero"), xe(n, "stroke-width", "2px"), Fe(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), Fe(i, "d", "M4.364,4.364L19.636,19.636"), xe(i, "fill", "none"), xe(i, "fill-rule", "nonzero"), xe(i, "stroke-width", "2px"), Fe(e, "width", "100%"), Fe(e, "height", "100%"), Fe(e, "viewBox", "0 0 24 24"), Fe(e, "version", "1.1"), Fe(e, "xmlns", "http://www.w3.org/2000/svg"), Fe(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), Fe(e, "xml:space", "preserve"), Fe(e, "stroke", "currentColor"), xe(e, "fill-rule", "evenodd"), xe(e, "clip-rule", "evenodd"), xe(e, "stroke-linecap", "round"), xe(e, "stroke-linejoin", "round");
    },
    m(o, s) {
      tf(o, e, s), Il(e, t), Il(t, n), Il(e, i);
    },
    p: Rl,
    i: Rl,
    o: Rl,
    d(o) {
      o && cn(e);
    }
  };
}
let of = class extends $s {
  constructor(e) {
    super(), ef(this, e, null, lf, nf, {});
  }
};
const {
  SvelteComponent: rf,
  append_hydration: af,
  attr: un,
  children: co,
  claim_svg_element: uo,
  detach: Dl,
  init: sf,
  insert_hydration: ff,
  noop: Nl,
  safe_not_equal: cf,
  svg_element: _o
} = window.__gradio__svelte__internal;
function uf(l) {
  let e, t;
  return {
    c() {
      e = _o("svg"), t = _o("path"), this.h();
    },
    l(n) {
      e = uo(n, "svg", {
        id: !0,
        xmlns: !0,
        viewBox: !0
      });
      var i = co(e);
      t = uo(i, "path", {
        d: !0,
        fill: !0
      }), co(t).forEach(Dl), i.forEach(Dl), this.h();
    },
    h() {
      un(t, "d", "M23,20a5,5,0,0,0-3.89,1.89L11.8,17.32a4.46,4.46,0,0,0,0-2.64l7.31-4.57A5,5,0,1,0,18,7a4.79,4.79,0,0,0,.2,1.32l-7.31,4.57a5,5,0,1,0,0,6.22l7.31,4.57A4.79,4.79,0,0,0,18,25a5,5,0,1,0,5-5ZM23,4a3,3,0,1,1-3,3A3,3,0,0,1,23,4ZM7,19a3,3,0,1,1,3-3A3,3,0,0,1,7,19Zm16,9a3,3,0,1,1,3-3A3,3,0,0,1,23,28Z"), un(t, "fill", "currentColor"), un(e, "id", "icon"), un(e, "xmlns", "http://www.w3.org/2000/svg"), un(e, "viewBox", "0 0 32 32");
    },
    m(n, i) {
      ff(n, e, i), af(e, t);
    },
    p: Nl,
    i: Nl,
    o: Nl,
    d(n) {
      n && Dl(e);
    }
  };
}
class _f extends rf {
  constructor(e) {
    super(), sf(this, e, null, uf, cf, {});
  }
}
const {
  SvelteComponent: df,
  append_hydration: mf,
  attr: Wt,
  children: mo,
  claim_svg_element: ho,
  detach: Ol,
  init: hf,
  insert_hydration: gf,
  noop: Ml,
  safe_not_equal: bf,
  svg_element: go
} = window.__gradio__svelte__internal;
function pf(l) {
  let e, t;
  return {
    c() {
      e = go("svg"), t = go("path"), this.h();
    },
    l(n) {
      e = ho(n, "svg", {
        xmlns: !0,
        width: !0,
        height: !0,
        viewBox: !0
      });
      var i = mo(e);
      t = ho(i, "path", {
        fill: !0,
        d: !0
      }), mo(t).forEach(Ol), i.forEach(Ol), this.h();
    },
    h() {
      Wt(t, "fill", "currentColor"), Wt(t, "d", "M26 24v4H6v-4H4v4a2 2 0 0 0 2 2h20a2 2 0 0 0 2-2v-4zm0-10l-1.41-1.41L17 20.17V2h-2v18.17l-7.59-7.58L6 14l10 10l10-10z"), Wt(e, "xmlns", "http://www.w3.org/2000/svg"), Wt(e, "width", "100%"), Wt(e, "height", "100%"), Wt(e, "viewBox", "0 0 32 32");
    },
    m(n, i) {
      gf(n, e, i), mf(e, t);
    },
    p: Ml,
    i: Ml,
    o: Ml,
    d(n) {
      n && Ol(e);
    }
  };
}
class zr extends df {
  constructor(e) {
    super(), hf(this, e, null, pf, bf, {});
  }
}
const {
  SvelteComponent: wf,
  append_hydration: kf,
  attr: ze,
  children: bo,
  claim_svg_element: po,
  detach: Pl,
  init: vf,
  insert_hydration: Ef,
  noop: Ul,
  safe_not_equal: yf,
  svg_element: wo
} = window.__gradio__svelte__internal;
function Tf(l) {
  let e, t;
  return {
    c() {
      e = wo("svg"), t = wo("path"), this.h();
    },
    l(n) {
      e = po(n, "svg", {
        xmlns: !0,
        width: !0,
        height: !0,
        viewBox: !0,
        fill: !0,
        stroke: !0,
        "stroke-width": !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0,
        class: !0
      });
      var i = bo(e);
      t = po(i, "path", {
        d: !0
      }), bo(t).forEach(Pl), i.forEach(Pl), this.h();
    },
    h() {
      ze(t, "d", "M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"), ze(e, "xmlns", "http://www.w3.org/2000/svg"), ze(e, "width", "100%"), ze(e, "height", "100%"), ze(e, "viewBox", "0 0 24 24"), ze(e, "fill", "none"), ze(e, "stroke", "currentColor"), ze(e, "stroke-width", "1.5"), ze(e, "stroke-linecap", "round"), ze(e, "stroke-linejoin", "round"), ze(e, "class", "feather feather-edit-2");
    },
    m(n, i) {
      Ef(n, e, i), kf(e, t);
    },
    p: Ul,
    i: Ul,
    o: Ul,
    d(n) {
      n && Pl(e);
    }
  };
}
class Af extends wf {
  constructor(e) {
    super(), vf(this, e, null, Tf, yf, {});
  }
}
const {
  SvelteComponent: Sf,
  append_hydration: Fl,
  attr: Q,
  children: jn,
  claim_svg_element: Hn,
  detach: _n,
  init: Cf,
  insert_hydration: Lf,
  noop: zl,
  safe_not_equal: If,
  svg_element: Vn
} = window.__gradio__svelte__internal;
function Rf(l) {
  let e, t, n, i;
  return {
    c() {
      e = Vn("svg"), t = Vn("rect"), n = Vn("circle"), i = Vn("polyline"), this.h();
    },
    l(o) {
      e = Hn(o, "svg", {
        xmlns: !0,
        width: !0,
        height: !0,
        viewBox: !0,
        fill: !0,
        stroke: !0,
        "stroke-width": !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0,
        class: !0
      });
      var s = jn(e);
      t = Hn(s, "rect", {
        x: !0,
        y: !0,
        width: !0,
        height: !0,
        rx: !0,
        ry: !0
      }), jn(t).forEach(_n), n = Hn(s, "circle", {
        cx: !0,
        cy: !0,
        r: !0
      }), jn(n).forEach(_n), i = Hn(s, "polyline", {
        points: !0
      }), jn(i).forEach(_n), s.forEach(_n), this.h();
    },
    h() {
      Q(t, "x", "3"), Q(t, "y", "3"), Q(t, "width", "18"), Q(t, "height", "18"), Q(t, "rx", "2"), Q(t, "ry", "2"), Q(n, "cx", "8.5"), Q(n, "cy", "8.5"), Q(n, "r", "1.5"), Q(i, "points", "21 15 16 10 5 21"), Q(e, "xmlns", "http://www.w3.org/2000/svg"), Q(e, "width", "100%"), Q(e, "height", "100%"), Q(e, "viewBox", "0 0 24 24"), Q(e, "fill", "none"), Q(e, "stroke", "currentColor"), Q(e, "stroke-width", "1.5"), Q(e, "stroke-linecap", "round"), Q(e, "stroke-linejoin", "round"), Q(e, "class", "feather feather-image");
    },
    m(o, s) {
      Lf(o, e, s), Fl(e, t), Fl(e, n), Fl(e, i);
    },
    p: zl,
    i: zl,
    o: zl,
    d(o) {
      o && _n(e);
    }
  };
}
let Br = class extends Sf {
  constructor(e) {
    super(), Cf(this, e, null, Rf, If, {});
  }
};
const {
  SvelteComponent: Df,
  append_hydration: ko,
  attr: se,
  children: Bl,
  claim_svg_element: ql,
  detach: Wn,
  init: Nf,
  insert_hydration: Of,
  noop: vo,
  safe_not_equal: Mf,
  svg_element: jl
} = window.__gradio__svelte__internal;
function Pf(l) {
  let e, t, n, i;
  return {
    c() {
      e = jl("svg"), t = jl("path"), n = jl("path"), this.h();
    },
    l(o) {
      e = ql(o, "svg", {
        xmlns: !0,
        viewBox: !0,
        fill: !0,
        "stroke-width": !0,
        color: !0
      });
      var s = Bl(e);
      t = ql(s, "path", {
        stroke: !0,
        "stroke-width": !0,
        "stroke-linecap": !0,
        d: !0
      }), Bl(t).forEach(Wn), n = ql(s, "path", {
        stroke: !0,
        "stroke-width": !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0,
        d: !0
      }), Bl(n).forEach(Wn), s.forEach(Wn), this.h();
    },
    h() {
      se(t, "stroke", "currentColor"), se(t, "stroke-width", "1.5"), se(t, "stroke-linecap", "round"), se(t, "d", "M16.472 20H4.1a.6.6 0 0 1-.6-.6V9.6a.6.6 0 0 1 .6-.6h2.768a2 2 0 0 0 1.715-.971l2.71-4.517a1.631 1.631 0 0 1 2.961 1.308l-1.022 3.408a.6.6 0 0 0 .574.772h4.575a2 2 0 0 1 1.93 2.526l-1.91 7A2 2 0 0 1 16.473 20Z"), se(n, "stroke", "currentColor"), se(n, "stroke-width", "1.5"), se(n, "stroke-linecap", "round"), se(n, "stroke-linejoin", "round"), se(n, "d", "M7 20V9"), se(e, "xmlns", "http://www.w3.org/2000/svg"), se(e, "viewBox", "0 0 24 24"), se(e, "fill", i = /*selected*/
      l[0] ? "currentColor" : "none"), se(e, "stroke-width", "1.5"), se(e, "color", "currentColor");
    },
    m(o, s) {
      Of(o, e, s), ko(e, t), ko(e, n);
    },
    p(o, [s]) {
      s & /*selected*/
      1 && i !== (i = /*selected*/
      o[0] ? "currentColor" : "none") && se(e, "fill", i);
    },
    i: vo,
    o: vo,
    d(o) {
      o && Wn(e);
    }
  };
}
function Uf(l, e, t) {
  let {
    selected: n
  } = e;
  return l.$$set = (i) => {
    "selected" in i && t(0, n = i.selected);
  }, [n];
}
class Ff extends Df {
  constructor(e) {
    super(), Nf(this, e, Uf, Pf, Mf, {
      selected: 0
    });
  }
}
const {
  SvelteComponent: zf,
  append_hydration: Eo,
  attr: Le,
  children: Hl,
  claim_svg_element: Vl,
  detach: Gn,
  init: Bf,
  insert_hydration: qf,
  noop: Wl,
  safe_not_equal: jf,
  svg_element: Gl
} = window.__gradio__svelte__internal;
function Hf(l) {
  let e, t, n;
  return {
    c() {
      e = Gl("svg"), t = Gl("polyline"), n = Gl("path"), this.h();
    },
    l(i) {
      e = Vl(i, "svg", {
        xmlns: !0,
        width: !0,
        height: !0,
        viewBox: !0,
        fill: !0,
        stroke: !0,
        "stroke-width": !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0,
        class: !0
      });
      var o = Hl(e);
      t = Vl(o, "polyline", {
        points: !0
      }), Hl(t).forEach(Gn), n = Vl(o, "path", {
        d: !0
      }), Hl(n).forEach(Gn), o.forEach(Gn), this.h();
    },
    h() {
      Le(t, "points", "1 4 1 10 7 10"), Le(n, "d", "M3.51 15a9 9 0 1 0 2.13-9.36L1 10"), Le(e, "xmlns", "http://www.w3.org/2000/svg"), Le(e, "width", "100%"), Le(e, "height", "100%"), Le(e, "viewBox", "0 0 24 24"), Le(e, "fill", "none"), Le(e, "stroke", "currentColor"), Le(e, "stroke-width", "2"), Le(e, "stroke-linecap", "round"), Le(e, "stroke-linejoin", "round"), Le(e, "class", "feather feather-rotate-ccw");
    },
    m(i, o) {
      qf(i, e, o), Eo(e, t), Eo(e, n);
    },
    p: Wl,
    i: Wl,
    o: Wl,
    d(i) {
      i && Gn(e);
    }
  };
}
class Vf extends zf {
  constructor(e) {
    super(), Bf(this, e, null, Hf, jf, {});
  }
}
const Wf = [{
  color: "red",
  primary: 600,
  secondary: 100
}, {
  color: "green",
  primary: 600,
  secondary: 100
}, {
  color: "blue",
  primary: 600,
  secondary: 100
}, {
  color: "yellow",
  primary: 500,
  secondary: 100
}, {
  color: "purple",
  primary: 600,
  secondary: 100
}, {
  color: "teal",
  primary: 600,
  secondary: 100
}, {
  color: "orange",
  primary: 600,
  secondary: 100
}, {
  color: "cyan",
  primary: 600,
  secondary: 100
}, {
  color: "lime",
  primary: 500,
  secondary: 100
}, {
  color: "pink",
  primary: 600,
  secondary: 100
}], yo = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Wf.reduce((l, {
  color: e,
  primary: t,
  secondary: n
}) => ({
  ...l,
  [e]: {
    primary: yo[e][t],
    secondary: yo[e][n]
  }
}), {});
class Gf extends Error {
  constructor(e) {
    super(e), this.name = "ShareError";
  }
}
const {
  SvelteComponent: Yf,
  claim_component: Xf,
  create_component: Zf,
  destroy_component: Kf,
  init: Jf,
  mount_component: Qf,
  safe_not_equal: xf,
  transition_in: $f,
  transition_out: ec
} = window.__gradio__svelte__internal, {
  createEventDispatcher: tc
} = window.__gradio__svelte__internal;
function nc(l) {
  let e, t;
  return e = new St({
    props: {
      Icon: _f,
      label: (
        /*i18n*/
        l[2]("common.share")
      ),
      pending: (
        /*pending*/
        l[3]
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    l[5]
  ), {
    c() {
      Zf(e.$$.fragment);
    },
    l(n) {
      Xf(e.$$.fragment, n);
    },
    m(n, i) {
      Qf(e, n, i), t = !0;
    },
    p(n, [i]) {
      const o = {};
      i & /*i18n*/
      4 && (o.label = /*i18n*/
      n[2]("common.share")), i & /*pending*/
      8 && (o.pending = /*pending*/
      n[3]), e.$set(o);
    },
    i(n) {
      t || ($f(e.$$.fragment, n), t = !0);
    },
    o(n) {
      ec(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Kf(e, n);
    }
  };
}
function lc(l, e, t) {
  const n = tc();
  let {
    formatter: i
  } = e, {
    value: o
  } = e, {
    i18n: s
  } = e, f = !1;
  const a = async () => {
    try {
      t(3, f = !0);
      const r = await i(o);
      n("share", {
        description: r
      });
    } catch (r) {
      console.error(r);
      let c = r instanceof Gf ? r.message : "Share failed.";
      n("error", c);
    } finally {
      t(3, f = !1);
    }
  };
  return l.$$set = (r) => {
    "formatter" in r && t(0, i = r.formatter), "value" in r && t(1, o = r.value), "i18n" in r && t(2, s = r.i18n);
  }, [i, o, s, f, n, a];
}
class ic extends Yf {
  constructor(e) {
    super(), Jf(this, e, lc, nc, xf, {
      formatter: 0,
      value: 1,
      i18n: 2
    });
  }
}
function Xt(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function tl() {
}
function oc(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const qr = typeof window < "u";
let To = qr ? () => window.performance.now() : () => Date.now(), jr = qr ? (l) => requestAnimationFrame(l) : tl;
const Jt = /* @__PURE__ */ new Set();
function Hr(l) {
  Jt.forEach((e) => {
    e.c(l) || (Jt.delete(e), e.f());
  }), Jt.size !== 0 && jr(Hr);
}
function rc(l) {
  let e;
  return Jt.size === 0 && jr(Hr), {
    promise: new Promise((t) => {
      Jt.add(e = {
        c: l,
        f: t
      });
    }),
    abort() {
      Jt.delete(e);
    }
  };
}
const Gt = [];
function ac(l, e = tl) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(f) {
    if (oc(l, f) && (l = f, t)) {
      const a = !Gt.length;
      for (const r of n)
        r[1](), Gt.push(r, l);
      if (a) {
        for (let r = 0; r < Gt.length; r += 2)
          Gt[r][0](Gt[r + 1]);
        Gt.length = 0;
      }
    }
  }
  function o(f) {
    i(f(l));
  }
  function s(f, a = tl) {
    const r = [f, a];
    return n.add(r), n.size === 1 && (t = e(i, o) || tl), f(l), () => {
      n.delete(r), n.size === 0 && t && (t(), t = null);
    };
  }
  return {
    set: i,
    update: o,
    subscribe: s
  };
}
function Ao(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function hi(l, e, t, n) {
  if (typeof t == "number" || Ao(t)) {
    const i = n - t, o = (t - e) / (l.dt || 1 / 60), s = l.opts.stiffness * i, f = l.opts.damping * o, a = (s - f) * l.inv_mass, r = (o + a) * l.dt;
    return Math.abs(r) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, Ao(t) ? new Date(t.getTime() + r) : t + r);
  } else {
    if (Array.isArray(t))
      return t.map((i, o) => hi(l, e[o], t[o], n[o]));
    if (typeof t == "object") {
      const i = {};
      for (const o in t)
        i[o] = hi(l, e[o], t[o], n[o]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function So(l, e = {}) {
  const t = ac(l), {
    stiffness: n = 0.15,
    damping: i = 0.8,
    precision: o = 0.01
  } = e;
  let s, f, a, r = l, c = l, u = 1, _ = 0, m = !1;
  function p(C, E = {}) {
    c = C;
    const b = a = {};
    return l == null || E.hard || y.stiffness >= 1 && y.damping >= 1 ? (m = !0, s = To(), r = C, t.set(l = c), Promise.resolve()) : (E.soft && (_ = 1 / ((E.soft === !0 ? 0.5 : +E.soft) * 60), u = 0), f || (s = To(), m = !1, f = rc((v) => {
      if (m)
        return m = !1, f = null, !1;
      u = Math.min(u + _, 1);
      const g = {
        inv_mass: u,
        opts: y,
        settled: !0,
        dt: (v - s) * 60 / 1e3
      }, S = hi(g, r, l, c);
      return s = v, r = l, t.set(l = S), g.settled && (f = null), !g.settled;
    })), new Promise((v) => {
      f.promise.then(() => {
        b === a && v();
      });
    }));
  }
  const y = {
    set: p,
    update: (C, E) => p(C(c, l), E),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: o
  };
  return y;
}
const {
  SvelteComponent: sc,
  append_hydration: Be,
  attr: U,
  children: Ie,
  claim_element: fc,
  claim_svg_element: qe,
  component_subscribe: Co,
  detach: Ee,
  element: cc,
  init: uc,
  insert_hydration: _c,
  noop: Lo,
  safe_not_equal: dc,
  set_style: Yn,
  svg_element: je,
  toggle_class: Io
} = window.__gradio__svelte__internal, {
  onMount: mc
} = window.__gradio__svelte__internal;
function hc(l) {
  let e, t, n, i, o, s, f, a, r, c, u, _;
  return {
    c() {
      e = cc("div"), t = je("svg"), n = je("g"), i = je("path"), o = je("path"), s = je("path"), f = je("path"), a = je("g"), r = je("path"), c = je("path"), u = je("path"), _ = je("path"), this.h();
    },
    l(m) {
      e = fc(m, "DIV", {
        class: !0
      });
      var p = Ie(e);
      t = qe(p, "svg", {
        viewBox: !0,
        fill: !0,
        xmlns: !0,
        class: !0
      });
      var y = Ie(t);
      n = qe(y, "g", {
        style: !0
      });
      var C = Ie(n);
      i = qe(C, "path", {
        d: !0,
        fill: !0,
        "fill-opacity": !0,
        class: !0
      }), Ie(i).forEach(Ee), o = qe(C, "path", {
        d: !0,
        fill: !0,
        class: !0
      }), Ie(o).forEach(Ee), s = qe(C, "path", {
        d: !0,
        fill: !0,
        "fill-opacity": !0,
        class: !0
      }), Ie(s).forEach(Ee), f = qe(C, "path", {
        d: !0,
        fill: !0,
        class: !0
      }), Ie(f).forEach(Ee), C.forEach(Ee), a = qe(y, "g", {
        style: !0
      });
      var E = Ie(a);
      r = qe(E, "path", {
        d: !0,
        fill: !0,
        "fill-opacity": !0,
        class: !0
      }), Ie(r).forEach(Ee), c = qe(E, "path", {
        d: !0,
        fill: !0,
        class: !0
      }), Ie(c).forEach(Ee), u = qe(E, "path", {
        d: !0,
        fill: !0,
        "fill-opacity": !0,
        class: !0
      }), Ie(u).forEach(Ee), _ = qe(E, "path", {
        d: !0,
        fill: !0,
        class: !0
      }), Ie(_).forEach(Ee), E.forEach(Ee), y.forEach(Ee), p.forEach(Ee), this.h();
    },
    h() {
      U(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), U(i, "fill", "#FF7C00"), U(i, "fill-opacity", "0.4"), U(i, "class", "svelte-43sxxs"), U(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), U(o, "fill", "#FF7C00"), U(o, "class", "svelte-43sxxs"), U(s, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), U(s, "fill", "#FF7C00"), U(s, "fill-opacity", "0.4"), U(s, "class", "svelte-43sxxs"), U(f, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), U(f, "fill", "#FF7C00"), U(f, "class", "svelte-43sxxs"), Yn(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), U(r, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), U(r, "fill", "#FF7C00"), U(r, "fill-opacity", "0.4"), U(r, "class", "svelte-43sxxs"), U(c, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), U(c, "fill", "#FF7C00"), U(c, "class", "svelte-43sxxs"), U(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), U(u, "fill", "#FF7C00"), U(u, "fill-opacity", "0.4"), U(u, "class", "svelte-43sxxs"), U(_, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), U(_, "fill", "#FF7C00"), U(_, "class", "svelte-43sxxs"), Yn(a, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), U(t, "viewBox", "-1200 -1200 3000 3000"), U(t, "fill", "none"), U(t, "xmlns", "http://www.w3.org/2000/svg"), U(t, "class", "svelte-43sxxs"), U(e, "class", "svelte-43sxxs"), Io(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(m, p) {
      _c(m, e, p), Be(e, t), Be(t, n), Be(n, i), Be(n, o), Be(n, s), Be(n, f), Be(t, a), Be(a, r), Be(a, c), Be(a, u), Be(a, _);
    },
    p(m, [p]) {
      p & /*$top*/
      2 && Yn(n, "transform", "translate(" + /*$top*/
      m[1][0] + "px, " + /*$top*/
      m[1][1] + "px)"), p & /*$bottom*/
      4 && Yn(a, "transform", "translate(" + /*$bottom*/
      m[2][0] + "px, " + /*$bottom*/
      m[2][1] + "px)"), p & /*margin*/
      1 && Io(
        e,
        "margin",
        /*margin*/
        m[0]
      );
    },
    i: Lo,
    o: Lo,
    d(m) {
      m && Ee(e);
    }
  };
}
function gc(l, e, t) {
  let n, i, {
    margin: o = !0
  } = e;
  const s = So([0, 0]);
  Co(l, s, (_) => t(1, n = _));
  const f = So([0, 0]);
  Co(l, f, (_) => t(2, i = _));
  let a;
  async function r() {
    await Promise.all([s.set([125, 140]), f.set([-125, -140])]), await Promise.all([s.set([-125, 140]), f.set([125, -140])]), await Promise.all([s.set([-125, 0]), f.set([125, -0])]), await Promise.all([s.set([125, 0]), f.set([-125, 0])]);
  }
  async function c() {
    await r(), a || c();
  }
  async function u() {
    await Promise.all([s.set([125, 0]), f.set([-125, 0])]), c();
  }
  return mc(() => (u(), () => a = !0)), l.$$set = (_) => {
    "margin" in _ && t(0, o = _.margin);
  }, [o, n, i, s, f];
}
class Vr extends sc {
  constructor(e) {
    super(), uc(this, e, gc, hc, dc, {
      margin: 0
    });
  }
}
const {
  SvelteComponent: bc,
  append_hydration: gi,
  attr: _t,
  bubble: pc,
  children: bi,
  claim_component: wc,
  claim_element: pi,
  claim_space: kc,
  claim_text: vc,
  create_component: Ec,
  destroy_component: yc,
  detach: kn,
  element: wi,
  init: Tc,
  insert_hydration: Wr,
  listen: Ac,
  mount_component: Sc,
  safe_not_equal: Cc,
  set_data: Lc,
  set_style: Yt,
  space: Ic,
  text: Rc,
  toggle_class: be,
  transition_in: Dc,
  transition_out: Nc
} = window.__gradio__svelte__internal;
function Ro(l) {
  let e, t;
  return {
    c() {
      e = wi("span"), t = Rc(
        /*label*/
        l[1]
      ), this.h();
    },
    l(n) {
      e = pi(n, "SPAN", {
        class: !0
      });
      var i = bi(e);
      t = vc(
        i,
        /*label*/
        l[1]
      ), i.forEach(kn), this.h();
    },
    h() {
      _t(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      Wr(n, e, i), gi(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && Lc(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && kn(e);
    }
  };
}
function Oc(l) {
  let e, t, n, i, o, s, f, a = (
    /*show_label*/
    l[2] && Ro(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = wi("button"), a && a.c(), t = Ic(), n = wi("div"), Ec(i.$$.fragment), this.h();
    },
    l(r) {
      e = pi(r, "BUTTON", {
        "aria-label": !0,
        "aria-haspopup": !0,
        title: !0,
        class: !0
      });
      var c = bi(e);
      a && a.l(c), t = kc(c), n = pi(c, "DIV", {
        class: !0
      });
      var u = bi(n);
      wc(i.$$.fragment, u), u.forEach(kn), c.forEach(kn), this.h();
    },
    h() {
      _t(n, "class", "svelte-1lrphxw"), be(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), be(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), be(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], _t(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), _t(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), _t(
        e,
        "title",
        /*label*/
        l[1]
      ), _t(e, "class", "svelte-1lrphxw"), be(
        e,
        "pending",
        /*pending*/
        l[3]
      ), be(
        e,
        "padded",
        /*padded*/
        l[5]
      ), be(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), be(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), Yt(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), Yt(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), Yt(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(r, c) {
      Wr(r, e, c), a && a.m(e, null), gi(e, t), gi(e, n), Sc(i, n, null), o = !0, s || (f = Ac(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), s = !0);
    },
    p(r, [c]) {
      /*show_label*/
      r[2] ? a ? a.p(r, c) : (a = Ro(r), a.c(), a.m(e, t)) : a && (a.d(1), a = null), (!o || c & /*size*/
      16) && be(
        n,
        "small",
        /*size*/
        r[4] === "small"
      ), (!o || c & /*size*/
      16) && be(
        n,
        "large",
        /*size*/
        r[4] === "large"
      ), (!o || c & /*size*/
      16) && be(
        n,
        "medium",
        /*size*/
        r[4] === "medium"
      ), (!o || c & /*disabled*/
      128) && (e.disabled = /*disabled*/
      r[7]), (!o || c & /*label*/
      2) && _t(
        e,
        "aria-label",
        /*label*/
        r[1]
      ), (!o || c & /*hasPopup*/
      256) && _t(
        e,
        "aria-haspopup",
        /*hasPopup*/
        r[8]
      ), (!o || c & /*label*/
      2) && _t(
        e,
        "title",
        /*label*/
        r[1]
      ), (!o || c & /*pending*/
      8) && be(
        e,
        "pending",
        /*pending*/
        r[3]
      ), (!o || c & /*padded*/
      32) && be(
        e,
        "padded",
        /*padded*/
        r[5]
      ), (!o || c & /*highlight*/
      64) && be(
        e,
        "highlight",
        /*highlight*/
        r[6]
      ), (!o || c & /*transparent*/
      512) && be(
        e,
        "transparent",
        /*transparent*/
        r[9]
      ), c & /*disabled, _color*/
      4224 && Yt(e, "color", !/*disabled*/
      r[7] && /*_color*/
      r[12] ? (
        /*_color*/
        r[12]
      ) : "var(--block-label-text-color)"), c & /*disabled, background*/
      1152 && Yt(e, "--bg-color", /*disabled*/
      r[7] ? "auto" : (
        /*background*/
        r[10]
      )), c & /*offset*/
      2048 && Yt(
        e,
        "margin-left",
        /*offset*/
        r[11] + "px"
      );
    },
    i(r) {
      o || (Dc(i.$$.fragment, r), o = !0);
    },
    o(r) {
      Nc(i.$$.fragment, r), o = !1;
    },
    d(r) {
      r && kn(e), a && a.d(), yc(i), s = !1, f();
    }
  };
}
function Mc(l, e, t) {
  let n, {
    Icon: i
  } = e, {
    label: o = ""
  } = e, {
    show_label: s = !1
  } = e, {
    pending: f = !1
  } = e, {
    size: a = "small"
  } = e, {
    padded: r = !0
  } = e, {
    highlight: c = !1
  } = e, {
    disabled: u = !1
  } = e, {
    hasPopup: _ = !1
  } = e, {
    color: m = "var(--block-label-text-color)"
  } = e, {
    transparent: p = !1
  } = e, {
    background: y = "var(--background-fill-primary)"
  } = e, {
    offset: C = 0
  } = e;
  function E(b) {
    pc.call(this, l, b);
  }
  return l.$$set = (b) => {
    "Icon" in b && t(0, i = b.Icon), "label" in b && t(1, o = b.label), "show_label" in b && t(2, s = b.show_label), "pending" in b && t(3, f = b.pending), "size" in b && t(4, a = b.size), "padded" in b && t(5, r = b.padded), "highlight" in b && t(6, c = b.highlight), "disabled" in b && t(7, u = b.disabled), "hasPopup" in b && t(8, _ = b.hasPopup), "color" in b && t(13, m = b.color), "transparent" in b && t(9, p = b.transparent), "background" in b && t(10, y = b.background), "offset" in b && t(11, C = b.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = c ? "var(--color-accent)" : m);
  }, [i, o, s, f, a, r, c, u, _, p, y, C, n, m, E];
}
class Pc extends bc {
  constructor(e) {
    super(), Tc(this, e, Mc, Oc, Cc, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: Uc,
  append_hydration: Yl,
  attr: He,
  children: Xn,
  claim_svg_element: Zn,
  detach: dn,
  init: Fc,
  insert_hydration: zc,
  noop: Xl,
  safe_not_equal: Bc,
  set_style: $e,
  svg_element: Kn
} = window.__gradio__svelte__internal;
function qc(l) {
  let e, t, n, i;
  return {
    c() {
      e = Kn("svg"), t = Kn("g"), n = Kn("path"), i = Kn("path"), this.h();
    },
    l(o) {
      e = Zn(o, "svg", {
        width: !0,
        height: !0,
        viewBox: !0,
        version: !0,
        xmlns: !0,
        "xmlns:xlink": !0,
        "xml:space": !0,
        stroke: !0,
        style: !0
      });
      var s = Xn(e);
      t = Zn(s, "g", {
        transform: !0
      });
      var f = Xn(t);
      n = Zn(f, "path", {
        d: !0,
        style: !0
      }), Xn(n).forEach(dn), f.forEach(dn), i = Zn(s, "path", {
        d: !0,
        style: !0
      }), Xn(i).forEach(dn), s.forEach(dn), this.h();
    },
    h() {
      He(n, "d", "M18,6L6.087,17.913"), $e(n, "fill", "none"), $e(n, "fill-rule", "nonzero"), $e(n, "stroke-width", "2px"), He(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), He(i, "d", "M4.364,4.364L19.636,19.636"), $e(i, "fill", "none"), $e(i, "fill-rule", "nonzero"), $e(i, "stroke-width", "2px"), He(e, "width", "100%"), He(e, "height", "100%"), He(e, "viewBox", "0 0 24 24"), He(e, "version", "1.1"), He(e, "xmlns", "http://www.w3.org/2000/svg"), He(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), He(e, "xml:space", "preserve"), He(e, "stroke", "currentColor"), $e(e, "fill-rule", "evenodd"), $e(e, "clip-rule", "evenodd"), $e(e, "stroke-linecap", "round"), $e(e, "stroke-linejoin", "round");
    },
    m(o, s) {
      zc(o, e, s), Yl(e, t), Yl(t, n), Yl(e, i);
    },
    p: Xl,
    i: Xl,
    o: Xl,
    d(o) {
      o && dn(e);
    }
  };
}
class jc extends Uc {
  constructor(e) {
    super(), Fc(this, e, null, qc, Bc, {});
  }
}
const {
  SvelteComponent: Hc,
  append_hydration: Lt,
  attr: Ye,
  binding_callbacks: Do,
  check_outros: ki,
  children: tt,
  claim_component: Gr,
  claim_element: nt,
  claim_space: Ne,
  claim_text: K,
  create_component: Yr,
  create_slot: Xr,
  destroy_component: Zr,
  destroy_each: Kr,
  detach: D,
  element: lt,
  empty: Me,
  ensure_array_like: ol,
  get_all_dirty_from_scope: Jr,
  get_slot_changes: Qr,
  group_outros: vi,
  init: Vc,
  insert_hydration: N,
  mount_component: xr,
  noop: Ei,
  safe_not_equal: Wc,
  set_data: Pe,
  set_style: At,
  space: Oe,
  text: J,
  toggle_class: Re,
  transition_in: Ge,
  transition_out: it,
  update_slot_base: $r
} = window.__gradio__svelte__internal, {
  tick: Gc
} = window.__gradio__svelte__internal, {
  onDestroy: Yc
} = window.__gradio__svelte__internal, {
  createEventDispatcher: Xc
} = window.__gradio__svelte__internal, Zc = (l) => ({}), No = (l) => ({}), Kc = (l) => ({}), Oo = (l) => ({});
function Mo(l, e, t) {
  const n = l.slice();
  return n[40] = e[t], n[42] = t, n;
}
function Po(l, e, t) {
  const n = l.slice();
  return n[40] = e[t], n;
}
function Jc(l) {
  let e, t, n, i, o = (
    /*i18n*/
    l[1]("common.error") + ""
  ), s, f, a;
  t = new Pc({
    props: {
      Icon: jc,
      label: (
        /*i18n*/
        l[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[32]
  );
  const r = (
    /*#slots*/
    l[30].error
  ), c = Xr(
    r,
    l,
    /*$$scope*/
    l[29],
    No
  );
  return {
    c() {
      e = lt("div"), Yr(t.$$.fragment), n = Oe(), i = lt("span"), s = J(o), f = Oe(), c && c.c(), this.h();
    },
    l(u) {
      e = nt(u, "DIV", {
        class: !0
      });
      var _ = tt(e);
      Gr(t.$$.fragment, _), _.forEach(D), n = Ne(u), i = nt(u, "SPAN", {
        class: !0
      });
      var m = tt(i);
      s = K(m, o), m.forEach(D), f = Ne(u), c && c.l(u), this.h();
    },
    h() {
      Ye(e, "class", "clear-status svelte-v0wucf"), Ye(i, "class", "error svelte-v0wucf");
    },
    m(u, _) {
      N(u, e, _), xr(t, e, null), N(u, n, _), N(u, i, _), Lt(i, s), N(u, f, _), c && c.m(u, _), a = !0;
    },
    p(u, _) {
      const m = {};
      _[0] & /*i18n*/
      2 && (m.label = /*i18n*/
      u[1]("common.clear")), t.$set(m), (!a || _[0] & /*i18n*/
      2) && o !== (o = /*i18n*/
      u[1]("common.error") + "") && Pe(s, o), c && c.p && (!a || _[0] & /*$$scope*/
      536870912) && $r(
        c,
        r,
        u,
        /*$$scope*/
        u[29],
        a ? Qr(
          r,
          /*$$scope*/
          u[29],
          _,
          Zc
        ) : Jr(
          /*$$scope*/
          u[29]
        ),
        No
      );
    },
    i(u) {
      a || (Ge(t.$$.fragment, u), Ge(c, u), a = !0);
    },
    o(u) {
      it(t.$$.fragment, u), it(c, u), a = !1;
    },
    d(u) {
      u && (D(e), D(n), D(i), D(f)), Zr(t), c && c.d(u);
    }
  };
}
function Qc(l) {
  let e, t, n, i, o, s, f, a, r, c = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && Uo(l)
  );
  function u(v, g) {
    if (
      /*progress*/
      v[7]
    ) return eu;
    if (
      /*queue_position*/
      v[2] !== null && /*queue_size*/
      v[3] !== void 0 && /*queue_position*/
      v[2] >= 0
    ) return $c;
    if (
      /*queue_position*/
      v[2] === 0
    ) return xc;
  }
  let _ = u(l), m = _ && _(l), p = (
    /*timer*/
    l[5] && Bo(l)
  );
  const y = [iu, lu], C = [];
  function E(v, g) {
    return (
      /*last_progress_level*/
      v[15] != null ? 0 : (
        /*show_progress*/
        v[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = E(l)) && (s = C[o] = y[o](l));
  let b = !/*timer*/
  l[5] && Yo(l);
  return {
    c() {
      c && c.c(), e = Oe(), t = lt("div"), m && m.c(), n = Oe(), p && p.c(), i = Oe(), s && s.c(), f = Oe(), b && b.c(), a = Me(), this.h();
    },
    l(v) {
      c && c.l(v), e = Ne(v), t = nt(v, "DIV", {
        class: !0
      });
      var g = tt(t);
      m && m.l(g), n = Ne(g), p && p.l(g), g.forEach(D), i = Ne(v), s && s.l(v), f = Ne(v), b && b.l(v), a = Me(), this.h();
    },
    h() {
      Ye(t, "class", "progress-text svelte-v0wucf"), Re(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), Re(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(v, g) {
      c && c.m(v, g), N(v, e, g), N(v, t, g), m && m.m(t, null), Lt(t, n), p && p.m(t, null), N(v, i, g), ~o && C[o].m(v, g), N(v, f, g), b && b.m(v, g), N(v, a, g), r = !0;
    },
    p(v, g) {
      /*variant*/
      v[8] === "default" && /*show_eta_bar*/
      v[18] && /*show_progress*/
      v[6] === "full" ? c ? c.p(v, g) : (c = Uo(v), c.c(), c.m(e.parentNode, e)) : c && (c.d(1), c = null), _ === (_ = u(v)) && m ? m.p(v, g) : (m && m.d(1), m = _ && _(v), m && (m.c(), m.m(t, n))), /*timer*/
      v[5] ? p ? p.p(v, g) : (p = Bo(v), p.c(), p.m(t, null)) : p && (p.d(1), p = null), (!r || g[0] & /*variant*/
      256) && Re(
        t,
        "meta-text-center",
        /*variant*/
        v[8] === "center"
      ), (!r || g[0] & /*variant*/
      256) && Re(
        t,
        "meta-text",
        /*variant*/
        v[8] === "default"
      );
      let S = o;
      o = E(v), o === S ? ~o && C[o].p(v, g) : (s && (vi(), it(C[S], 1, 1, () => {
        C[S] = null;
      }), ki()), ~o ? (s = C[o], s ? s.p(v, g) : (s = C[o] = y[o](v), s.c()), Ge(s, 1), s.m(f.parentNode, f)) : s = null), /*timer*/
      v[5] ? b && (vi(), it(b, 1, 1, () => {
        b = null;
      }), ki()) : b ? (b.p(v, g), g[0] & /*timer*/
      32 && Ge(b, 1)) : (b = Yo(v), b.c(), Ge(b, 1), b.m(a.parentNode, a));
    },
    i(v) {
      r || (Ge(s), Ge(b), r = !0);
    },
    o(v) {
      it(s), it(b), r = !1;
    },
    d(v) {
      v && (D(e), D(t), D(i), D(f), D(a)), c && c.d(v), m && m.d(), p && p.d(), ~o && C[o].d(v), b && b.d(v);
    }
  };
}
function Uo(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = lt("div"), this.h();
    },
    l(n) {
      e = nt(n, "DIV", {
        class: !0
      }), tt(e).forEach(D), this.h();
    },
    h() {
      Ye(e, "class", "eta-bar svelte-v0wucf"), At(e, "transform", t);
    },
    m(n, i) {
      N(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && At(e, "transform", t);
    },
    d(n) {
      n && D(e);
    }
  };
}
function xc(l) {
  let e;
  return {
    c() {
      e = J("processing |");
    },
    l(t) {
      e = K(t, "processing |");
    },
    m(t, n) {
      N(t, e, n);
    },
    p: Ei,
    d(t) {
      t && D(e);
    }
  };
}
function $c(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, o, s;
  return {
    c() {
      e = J("queue: "), n = J(t), i = J("/"), o = J(
        /*queue_size*/
        l[3]
      ), s = J(" |");
    },
    l(f) {
      e = K(f, "queue: "), n = K(f, t), i = K(f, "/"), o = K(
        f,
        /*queue_size*/
        l[3]
      ), s = K(f, " |");
    },
    m(f, a) {
      N(f, e, a), N(f, n, a), N(f, i, a), N(f, o, a), N(f, s, a);
    },
    p(f, a) {
      a[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      f[2] + 1 + "") && Pe(n, t), a[0] & /*queue_size*/
      8 && Pe(
        o,
        /*queue_size*/
        f[3]
      );
    },
    d(f) {
      f && (D(e), D(n), D(i), D(o), D(s));
    }
  };
}
function eu(l) {
  let e, t = ol(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = zo(Po(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Me();
    },
    l(i) {
      for (let o = 0; o < n.length; o += 1)
        n[o].l(i);
      e = Me();
    },
    m(i, o) {
      for (let s = 0; s < n.length; s += 1)
        n[s] && n[s].m(i, o);
      N(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress*/
      128) {
        t = ol(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const f = Po(i, t, s);
          n[s] ? n[s].p(f, o) : (n[s] = zo(f), n[s].c(), n[s].m(e.parentNode, e));
        }
        for (; s < n.length; s += 1)
          n[s].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && D(e), Kr(n, i);
    }
  };
}
function Fo(l) {
  let e, t = (
    /*p*/
    l[40].unit + ""
  ), n, i, o = " ", s;
  function f(c, u) {
    return (
      /*p*/
      c[40].length != null ? nu : tu
    );
  }
  let a = f(l), r = a(l);
  return {
    c() {
      r.c(), e = Oe(), n = J(t), i = J(" | "), s = J(o);
    },
    l(c) {
      r.l(c), e = Ne(c), n = K(c, t), i = K(c, " | "), s = K(c, o);
    },
    m(c, u) {
      r.m(c, u), N(c, e, u), N(c, n, u), N(c, i, u), N(c, s, u);
    },
    p(c, u) {
      a === (a = f(c)) && r ? r.p(c, u) : (r.d(1), r = a(c), r && (r.c(), r.m(e.parentNode, e))), u[0] & /*progress*/
      128 && t !== (t = /*p*/
      c[40].unit + "") && Pe(n, t);
    },
    d(c) {
      c && (D(e), D(n), D(i), D(s)), r.d(c);
    }
  };
}
function tu(l) {
  let e = Xt(
    /*p*/
    l[40].index || 0
  ) + "", t;
  return {
    c() {
      t = J(e);
    },
    l(n) {
      t = K(n, e);
    },
    m(n, i) {
      N(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = Xt(
        /*p*/
        n[40].index || 0
      ) + "") && Pe(t, e);
    },
    d(n) {
      n && D(t);
    }
  };
}
function nu(l) {
  let e = Xt(
    /*p*/
    l[40].index || 0
  ) + "", t, n, i = Xt(
    /*p*/
    l[40].length
  ) + "", o;
  return {
    c() {
      t = J(e), n = J("/"), o = J(i);
    },
    l(s) {
      t = K(s, e), n = K(s, "/"), o = K(s, i);
    },
    m(s, f) {
      N(s, t, f), N(s, n, f), N(s, o, f);
    },
    p(s, f) {
      f[0] & /*progress*/
      128 && e !== (e = Xt(
        /*p*/
        s[40].index || 0
      ) + "") && Pe(t, e), f[0] & /*progress*/
      128 && i !== (i = Xt(
        /*p*/
        s[40].length
      ) + "") && Pe(o, i);
    },
    d(s) {
      s && (D(t), D(n), D(o));
    }
  };
}
function zo(l) {
  let e, t = (
    /*p*/
    l[40].index != null && Fo(l)
  );
  return {
    c() {
      t && t.c(), e = Me();
    },
    l(n) {
      t && t.l(n), e = Me();
    },
    m(n, i) {
      t && t.m(n, i), N(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[40].index != null ? t ? t.p(n, i) : (t = Fo(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && D(e), t && t.d(n);
    }
  };
}
function Bo(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = J(
        /*formatted_timer*/
        l[20]
      ), n = J(t), i = J("s");
    },
    l(o) {
      e = K(
        o,
        /*formatted_timer*/
        l[20]
      ), n = K(o, t), i = K(o, "s");
    },
    m(o, s) {
      N(o, e, s), N(o, n, s), N(o, i, s);
    },
    p(o, s) {
      s[0] & /*formatted_timer*/
      1048576 && Pe(
        e,
        /*formatted_timer*/
        o[20]
      ), s[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && Pe(n, t);
    },
    d(o) {
      o && (D(e), D(n), D(i));
    }
  };
}
function lu(l) {
  let e, t;
  return e = new Vr({
    props: {
      margin: (
        /*variant*/
        l[8] === "default"
      )
    }
  }), {
    c() {
      Yr(e.$$.fragment);
    },
    l(n) {
      Gr(e.$$.fragment, n);
    },
    m(n, i) {
      xr(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*variant*/
      256 && (o.margin = /*variant*/
      n[8] === "default"), e.$set(o);
    },
    i(n) {
      t || (Ge(e.$$.fragment, n), t = !0);
    },
    o(n) {
      it(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Zr(e, n);
    }
  };
}
function iu(l) {
  let e, t, n, i, o, s = `${/*last_progress_level*/
  l[15] * 100}%`, f = (
    /*progress*/
    l[7] != null && qo(l)
  );
  return {
    c() {
      e = lt("div"), t = lt("div"), f && f.c(), n = Oe(), i = lt("div"), o = lt("div"), this.h();
    },
    l(a) {
      e = nt(a, "DIV", {
        class: !0
      });
      var r = tt(e);
      t = nt(r, "DIV", {
        class: !0
      });
      var c = tt(t);
      f && f.l(c), c.forEach(D), n = Ne(r), i = nt(r, "DIV", {
        class: !0
      });
      var u = tt(i);
      o = nt(u, "DIV", {
        class: !0
      }), tt(o).forEach(D), u.forEach(D), r.forEach(D), this.h();
    },
    h() {
      Ye(t, "class", "progress-level-inner svelte-v0wucf"), Ye(o, "class", "progress-bar svelte-v0wucf"), At(o, "width", s), Ye(i, "class", "progress-bar-wrap svelte-v0wucf"), Ye(e, "class", "progress-level svelte-v0wucf");
    },
    m(a, r) {
      N(a, e, r), Lt(e, t), f && f.m(t, null), Lt(e, n), Lt(e, i), Lt(i, o), l[31](o);
    },
    p(a, r) {
      /*progress*/
      a[7] != null ? f ? f.p(a, r) : (f = qo(a), f.c(), f.m(t, null)) : f && (f.d(1), f = null), r[0] & /*last_progress_level*/
      32768 && s !== (s = `${/*last_progress_level*/
      a[15] * 100}%`) && At(o, "width", s);
    },
    i: Ei,
    o: Ei,
    d(a) {
      a && D(e), f && f.d(), l[31](null);
    }
  };
}
function qo(l) {
  let e, t = ol(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Go(Mo(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Me();
    },
    l(i) {
      for (let o = 0; o < n.length; o += 1)
        n[o].l(i);
      e = Me();
    },
    m(i, o) {
      for (let s = 0; s < n.length; s += 1)
        n[s] && n[s].m(i, o);
      N(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        t = ol(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const f = Mo(i, t, s);
          n[s] ? n[s].p(f, o) : (n[s] = Go(f), n[s].c(), n[s].m(e.parentNode, e));
        }
        for (; s < n.length; s += 1)
          n[s].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && D(e), Kr(n, i);
    }
  };
}
function jo(l) {
  let e, t, n, i, o = (
    /*i*/
    l[42] !== 0 && ou()
  ), s = (
    /*p*/
    l[40].desc != null && Ho(l)
  ), f = (
    /*p*/
    l[40].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[42]
    ] != null && Vo()
  ), a = (
    /*progress_level*/
    l[14] != null && Wo(l)
  );
  return {
    c() {
      o && o.c(), e = Oe(), s && s.c(), t = Oe(), f && f.c(), n = Oe(), a && a.c(), i = Me();
    },
    l(r) {
      o && o.l(r), e = Ne(r), s && s.l(r), t = Ne(r), f && f.l(r), n = Ne(r), a && a.l(r), i = Me();
    },
    m(r, c) {
      o && o.m(r, c), N(r, e, c), s && s.m(r, c), N(r, t, c), f && f.m(r, c), N(r, n, c), a && a.m(r, c), N(r, i, c);
    },
    p(r, c) {
      /*p*/
      r[40].desc != null ? s ? s.p(r, c) : (s = Ho(r), s.c(), s.m(t.parentNode, t)) : s && (s.d(1), s = null), /*p*/
      r[40].desc != null && /*progress_level*/
      r[14] && /*progress_level*/
      r[14][
        /*i*/
        r[42]
      ] != null ? f || (f = Vo(), f.c(), f.m(n.parentNode, n)) : f && (f.d(1), f = null), /*progress_level*/
      r[14] != null ? a ? a.p(r, c) : (a = Wo(r), a.c(), a.m(i.parentNode, i)) : a && (a.d(1), a = null);
    },
    d(r) {
      r && (D(e), D(t), D(n), D(i)), o && o.d(r), s && s.d(r), f && f.d(r), a && a.d(r);
    }
  };
}
function ou(l) {
  let e;
  return {
    c() {
      e = J(" /");
    },
    l(t) {
      e = K(t, " /");
    },
    m(t, n) {
      N(t, e, n);
    },
    d(t) {
      t && D(e);
    }
  };
}
function Ho(l) {
  let e = (
    /*p*/
    l[40].desc + ""
  ), t;
  return {
    c() {
      t = J(e);
    },
    l(n) {
      t = K(n, e);
    },
    m(n, i) {
      N(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[40].desc + "") && Pe(t, e);
    },
    d(n) {
      n && D(t);
    }
  };
}
function Vo(l) {
  let e;
  return {
    c() {
      e = J("-");
    },
    l(t) {
      e = K(t, "-");
    },
    m(t, n) {
      N(t, e, n);
    },
    d(t) {
      t && D(e);
    }
  };
}
function Wo(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[42]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = J(e), n = J("%");
    },
    l(i) {
      t = K(i, e), n = K(i, "%");
    },
    m(i, o) {
      N(i, t, o), N(i, n, o);
    },
    p(i, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[42]
      ] || 0)).toFixed(1) + "") && Pe(t, e);
    },
    d(i) {
      i && (D(t), D(n));
    }
  };
}
function Go(l) {
  let e, t = (
    /*p*/
    (l[40].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[42]
    ] != null) && jo(l)
  );
  return {
    c() {
      t && t.c(), e = Me();
    },
    l(n) {
      t && t.l(n), e = Me();
    },
    m(n, i) {
      t && t.m(n, i), N(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[40].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[42]
      ] != null ? t ? t.p(n, i) : (t = jo(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && D(e), t && t.d(n);
    }
  };
}
function Yo(l) {
  let e, t, n, i;
  const o = (
    /*#slots*/
    l[30]["additional-loading-text"]
  ), s = Xr(
    o,
    l,
    /*$$scope*/
    l[29],
    Oo
  );
  return {
    c() {
      e = lt("p"), t = J(
        /*loading_text*/
        l[9]
      ), n = Oe(), s && s.c(), this.h();
    },
    l(f) {
      e = nt(f, "P", {
        class: !0
      });
      var a = tt(e);
      t = K(
        a,
        /*loading_text*/
        l[9]
      ), a.forEach(D), n = Ne(f), s && s.l(f), this.h();
    },
    h() {
      Ye(e, "class", "loading svelte-v0wucf");
    },
    m(f, a) {
      N(f, e, a), Lt(e, t), N(f, n, a), s && s.m(f, a), i = !0;
    },
    p(f, a) {
      (!i || a[0] & /*loading_text*/
      512) && Pe(
        t,
        /*loading_text*/
        f[9]
      ), s && s.p && (!i || a[0] & /*$$scope*/
      536870912) && $r(
        s,
        o,
        f,
        /*$$scope*/
        f[29],
        i ? Qr(
          o,
          /*$$scope*/
          f[29],
          a,
          Kc
        ) : Jr(
          /*$$scope*/
          f[29]
        ),
        Oo
      );
    },
    i(f) {
      i || (Ge(s, f), i = !0);
    },
    o(f) {
      it(s, f), i = !1;
    },
    d(f) {
      f && (D(e), D(n)), s && s.d(f);
    }
  };
}
function ru(l) {
  let e, t, n, i, o;
  const s = [Qc, Jc], f = [];
  function a(r, c) {
    return (
      /*status*/
      r[4] === "pending" ? 0 : (
        /*status*/
        r[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = a(l)) && (n = f[t] = s[t](l)), {
    c() {
      e = lt("div"), n && n.c(), this.h();
    },
    l(r) {
      e = nt(r, "DIV", {
        class: !0
      });
      var c = tt(e);
      n && n.l(c), c.forEach(D), this.h();
    },
    h() {
      Ye(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-v0wucf"), Re(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), Re(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), Re(
        e,
        "generating",
        /*status*/
        l[4] === "generating" && /*show_progress*/
        l[6] === "full"
      ), Re(
        e,
        "border",
        /*border*/
        l[12]
      ), At(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), At(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(r, c) {
      N(r, e, c), ~t && f[t].m(e, null), l[33](e), o = !0;
    },
    p(r, c) {
      let u = t;
      t = a(r), t === u ? ~t && f[t].p(r, c) : (n && (vi(), it(f[u], 1, 1, () => {
        f[u] = null;
      }), ki()), ~t ? (n = f[t], n ? n.p(r, c) : (n = f[t] = s[t](r), n.c()), Ge(n, 1), n.m(e, null)) : n = null), (!o || c[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      r[8] + " " + /*show_progress*/
      r[6] + " svelte-v0wucf")) && Ye(e, "class", i), (!o || c[0] & /*variant, show_progress, status, show_progress*/
      336) && Re(e, "hide", !/*status*/
      r[4] || /*status*/
      r[4] === "complete" || /*show_progress*/
      r[6] === "hidden"), (!o || c[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && Re(
        e,
        "translucent",
        /*variant*/
        r[8] === "center" && /*status*/
        (r[4] === "pending" || /*status*/
        r[4] === "error") || /*translucent*/
        r[11] || /*show_progress*/
        r[6] === "minimal"
      ), (!o || c[0] & /*variant, show_progress, status, show_progress*/
      336) && Re(
        e,
        "generating",
        /*status*/
        r[4] === "generating" && /*show_progress*/
        r[6] === "full"
      ), (!o || c[0] & /*variant, show_progress, border*/
      4416) && Re(
        e,
        "border",
        /*border*/
        r[12]
      ), c[0] & /*absolute*/
      1024 && At(
        e,
        "position",
        /*absolute*/
        r[10] ? "absolute" : "static"
      ), c[0] & /*absolute*/
      1024 && At(
        e,
        "padding",
        /*absolute*/
        r[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(r) {
      o || (Ge(n), o = !0);
    },
    o(r) {
      it(n), o = !1;
    },
    d(r) {
      r && D(e), ~t && f[t].d(), l[33](null);
    }
  };
}
let Jn = [], Zl = !1;
async function au(l, e = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
    if (Jn.push(l), !Zl) Zl = !0;
    else return;
    await Gc(), requestAnimationFrame(() => {
      let t = [0, 0];
      for (let n = 0; n < Jn.length; n++) {
        const o = Jn[n].getBoundingClientRect();
        (n === 0 || o.top + window.scrollY <= t[0]) && (t[0] = o.top + window.scrollY, t[1] = n);
      }
      window.scrollTo({
        top: t[0] - 20,
        behavior: "smooth"
      }), Zl = !1, Jn = [];
    });
  }
}
function su(l, e, t) {
  let n, {
    $$slots: i = {},
    $$scope: o
  } = e;
  const s = Xc();
  let {
    i18n: f
  } = e, {
    eta: a = null
  } = e, {
    queue_position: r
  } = e, {
    queue_size: c
  } = e, {
    status: u
  } = e, {
    scroll_to_output: _ = !1
  } = e, {
    timer: m = !0
  } = e, {
    show_progress: p = "full"
  } = e, {
    message: y = null
  } = e, {
    progress: C = null
  } = e, {
    variant: E = "default"
  } = e, {
    loading_text: b = "Loading..."
  } = e, {
    absolute: v = !0
  } = e, {
    translucent: g = !1
  } = e, {
    border: S = !1
  } = e, {
    autoscroll: w
  } = e, L, A = !1, q = 0, F = 0, P = null, j = null, de = 0, x = null, Ae, ee = null, ke = !0;
  const Se = () => {
    t(0, a = t(27, P = t(19, z = null))), t(25, q = performance.now()), t(26, F = 0), A = !0, re();
  };
  function re() {
    requestAnimationFrame(() => {
      t(26, F = (performance.now() - q) / 1e3), A && re();
    });
  }
  function G() {
    t(26, F = 0), t(0, a = t(27, P = t(19, z = null))), A && (A = !1);
  }
  Yc(() => {
    A && G();
  });
  let z = null;
  function Ze(h) {
    Do[h ? "unshift" : "push"](() => {
      ee = h, t(16, ee), t(7, C), t(14, x), t(15, Ae);
    });
  }
  const W = () => {
    s("clear_status");
  };
  function wt(h) {
    Do[h ? "unshift" : "push"](() => {
      L = h, t(13, L);
    });
  }
  return l.$$set = (h) => {
    "i18n" in h && t(1, f = h.i18n), "eta" in h && t(0, a = h.eta), "queue_position" in h && t(2, r = h.queue_position), "queue_size" in h && t(3, c = h.queue_size), "status" in h && t(4, u = h.status), "scroll_to_output" in h && t(22, _ = h.scroll_to_output), "timer" in h && t(5, m = h.timer), "show_progress" in h && t(6, p = h.show_progress), "message" in h && t(23, y = h.message), "progress" in h && t(7, C = h.progress), "variant" in h && t(8, E = h.variant), "loading_text" in h && t(9, b = h.loading_text), "absolute" in h && t(10, v = h.absolute), "translucent" in h && t(11, g = h.translucent), "border" in h && t(12, S = h.border), "autoscroll" in h && t(24, w = h.autoscroll), "$$scope" in h && t(29, o = h.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (a === null && t(0, a = P), a != null && P !== a && (t(28, j = (performance.now() - q) / 1e3 + a), t(19, z = j.toFixed(1)), t(27, P = a))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, de = j === null || j <= 0 || !F ? null : Math.min(F / j, 1)), l.$$.dirty[0] & /*progress*/
    128 && C != null && t(18, ke = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (C != null ? t(14, x = C.map((h) => {
      if (h.index != null && h.length != null)
        return h.index / h.length;
      if (h.progress != null)
        return h.progress;
    })) : t(14, x = null), x ? (t(15, Ae = x[x.length - 1]), ee && (Ae === 0 ? t(16, ee.style.transition = "0", ee) : t(16, ee.style.transition = "150ms", ee))) : t(15, Ae = void 0)), l.$$.dirty[0] & /*status*/
    16 && (u === "pending" ? Se() : G()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && L && _ && (u === "pending" || u === "complete") && au(L, w), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = F.toFixed(1));
  }, [a, f, r, c, u, m, p, C, E, b, v, g, S, L, x, Ae, ee, de, ke, z, n, s, _, y, w, q, F, P, j, o, i, Ze, W, wt];
}
class fu extends Hc {
  constructor(e) {
    super(), Vc(this, e, su, ru, Wc, {
      i18n: 1,
      eta: 0,
      queue_position: 2,
      queue_size: 3,
      status: 4,
      scroll_to_output: 22,
      timer: 5,
      show_progress: 6,
      message: 23,
      progress: 7,
      variant: 8,
      loading_text: 9,
      absolute: 10,
      translucent: 11,
      border: 12,
      autoscroll: 24
    }, null, [-1, -1]);
  }
}
/*! @license DOMPurify 3.1.6 | (c) Cure53 and other contributors | Released under the Apache license 2.0 and Mozilla Public License 2.0 | github.com/cure53/DOMPurify/blob/3.1.6/LICENSE */
const {
  entries: ea,
  setPrototypeOf: Xo,
  isFrozen: cu,
  getPrototypeOf: uu,
  getOwnPropertyDescriptor: _u
} = Object;
let {
  freeze: _e,
  seal: Ue,
  create: ta
} = Object, {
  apply: yi,
  construct: Ti
} = typeof Reflect < "u" && Reflect;
_e || (_e = function(e) {
  return e;
});
Ue || (Ue = function(e) {
  return e;
});
yi || (yi = function(e, t, n) {
  return e.apply(t, n);
});
Ti || (Ti = function(e, t) {
  return new e(...t);
});
const Qn = Te(Array.prototype.forEach), Zo = Te(Array.prototype.pop), mn = Te(Array.prototype.push), nl = Te(String.prototype.toLowerCase), Kl = Te(String.prototype.toString), Ko = Te(String.prototype.match), hn = Te(String.prototype.replace), du = Te(String.prototype.indexOf), mu = Te(String.prototype.trim), Ve = Te(Object.prototype.hasOwnProperty), fe = Te(RegExp.prototype.test), gn = hu(TypeError);
function Te(l) {
  return function(e) {
    for (var t = arguments.length, n = new Array(t > 1 ? t - 1 : 0), i = 1; i < t; i++)
      n[i - 1] = arguments[i];
    return yi(l, e, n);
  };
}
function hu(l) {
  return function() {
    for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
      t[n] = arguments[n];
    return Ti(l, t);
  };
}
function O(l, e) {
  let t = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : nl;
  Xo && Xo(l, null);
  let n = e.length;
  for (; n--; ) {
    let i = e[n];
    if (typeof i == "string") {
      const o = t(i);
      o !== i && (cu(e) || (e[n] = o), i = o);
    }
    l[i] = !0;
  }
  return l;
}
function gu(l) {
  for (let e = 0; e < l.length; e++)
    Ve(l, e) || (l[e] = null);
  return l;
}
function Ct(l) {
  const e = ta(null);
  for (const [t, n] of ea(l))
    Ve(l, t) && (Array.isArray(n) ? e[t] = gu(n) : n && typeof n == "object" && n.constructor === Object ? e[t] = Ct(n) : e[t] = n);
  return e;
}
function bn(l, e) {
  for (; l !== null; ) {
    const n = _u(l, e);
    if (n) {
      if (n.get)
        return Te(n.get);
      if (typeof n.value == "function")
        return Te(n.value);
    }
    l = uu(l);
  }
  function t() {
    return null;
  }
  return t;
}
const Jo = _e(["a", "abbr", "acronym", "address", "area", "article", "aside", "audio", "b", "bdi", "bdo", "big", "blink", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite", "code", "col", "colgroup", "content", "data", "datalist", "dd", "decorator", "del", "details", "dfn", "dialog", "dir", "div", "dl", "dt", "element", "em", "fieldset", "figcaption", "figure", "font", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "img", "input", "ins", "kbd", "label", "legend", "li", "main", "map", "mark", "marquee", "menu", "menuitem", "meter", "nav", "nobr", "ol", "optgroup", "option", "output", "p", "picture", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "section", "select", "shadow", "small", "source", "spacer", "span", "strike", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "tr", "track", "tt", "u", "ul", "var", "video", "wbr"]), Jl = _e(["svg", "a", "altglyph", "altglyphdef", "altglyphitem", "animatecolor", "animatemotion", "animatetransform", "circle", "clippath", "defs", "desc", "ellipse", "filter", "font", "g", "glyph", "glyphref", "hkern", "image", "line", "lineargradient", "marker", "mask", "metadata", "mpath", "path", "pattern", "polygon", "polyline", "radialgradient", "rect", "stop", "style", "switch", "symbol", "text", "textpath", "title", "tref", "tspan", "view", "vkern"]), Ql = _e(["feBlend", "feColorMatrix", "feComponentTransfer", "feComposite", "feConvolveMatrix", "feDiffuseLighting", "feDisplacementMap", "feDistantLight", "feDropShadow", "feFlood", "feFuncA", "feFuncB", "feFuncG", "feFuncR", "feGaussianBlur", "feImage", "feMerge", "feMergeNode", "feMorphology", "feOffset", "fePointLight", "feSpecularLighting", "feSpotLight", "feTile", "feTurbulence"]), bu = _e(["animate", "color-profile", "cursor", "discard", "font-face", "font-face-format", "font-face-name", "font-face-src", "font-face-uri", "foreignobject", "hatch", "hatchpath", "mesh", "meshgradient", "meshpatch", "meshrow", "missing-glyph", "script", "set", "solidcolor", "unknown", "use"]), xl = _e(["math", "menclose", "merror", "mfenced", "mfrac", "mglyph", "mi", "mlabeledtr", "mmultiscripts", "mn", "mo", "mover", "mpadded", "mphantom", "mroot", "mrow", "ms", "mspace", "msqrt", "mstyle", "msub", "msup", "msubsup", "mtable", "mtd", "mtext", "mtr", "munder", "munderover", "mprescripts"]), pu = _e(["maction", "maligngroup", "malignmark", "mlongdiv", "mscarries", "mscarry", "msgroup", "mstack", "msline", "msrow", "semantics", "annotation", "annotation-xml", "mprescripts", "none"]), Qo = _e(["#text"]), xo = _e(["accept", "action", "align", "alt", "autocapitalize", "autocomplete", "autopictureinpicture", "autoplay", "background", "bgcolor", "border", "capture", "cellpadding", "cellspacing", "checked", "cite", "class", "clear", "color", "cols", "colspan", "controls", "controlslist", "coords", "crossorigin", "datetime", "decoding", "default", "dir", "disabled", "disablepictureinpicture", "disableremoteplayback", "download", "draggable", "enctype", "enterkeyhint", "face", "for", "headers", "height", "hidden", "high", "href", "hreflang", "id", "inputmode", "integrity", "ismap", "kind", "label", "lang", "list", "loading", "loop", "low", "max", "maxlength", "media", "method", "min", "minlength", "multiple", "muted", "name", "nonce", "noshade", "novalidate", "nowrap", "open", "optimum", "pattern", "placeholder", "playsinline", "popover", "popovertarget", "popovertargetaction", "poster", "preload", "pubdate", "radiogroup", "readonly", "rel", "required", "rev", "reversed", "role", "rows", "rowspan", "spellcheck", "scope", "selected", "shape", "size", "sizes", "span", "srclang", "start", "src", "srcset", "step", "style", "summary", "tabindex", "title", "translate", "type", "usemap", "valign", "value", "width", "wrap", "xmlns", "slot"]), $l = _e(["accent-height", "accumulate", "additive", "alignment-baseline", "ascent", "attributename", "attributetype", "azimuth", "basefrequency", "baseline-shift", "begin", "bias", "by", "class", "clip", "clippathunits", "clip-path", "clip-rule", "color", "color-interpolation", "color-interpolation-filters", "color-profile", "color-rendering", "cx", "cy", "d", "dx", "dy", "diffuseconstant", "direction", "display", "divisor", "dur", "edgemode", "elevation", "end", "fill", "fill-opacity", "fill-rule", "filter", "filterunits", "flood-color", "flood-opacity", "font-family", "font-size", "font-size-adjust", "font-stretch", "font-style", "font-variant", "font-weight", "fx", "fy", "g1", "g2", "glyph-name", "glyphref", "gradientunits", "gradienttransform", "height", "href", "id", "image-rendering", "in", "in2", "k", "k1", "k2", "k3", "k4", "kerning", "keypoints", "keysplines", "keytimes", "lang", "lengthadjust", "letter-spacing", "kernelmatrix", "kernelunitlength", "lighting-color", "local", "marker-end", "marker-mid", "marker-start", "markerheight", "markerunits", "markerwidth", "maskcontentunits", "maskunits", "max", "mask", "media", "method", "mode", "min", "name", "numoctaves", "offset", "operator", "opacity", "order", "orient", "orientation", "origin", "overflow", "paint-order", "path", "pathlength", "patterncontentunits", "patterntransform", "patternunits", "points", "preservealpha", "preserveaspectratio", "primitiveunits", "r", "rx", "ry", "radius", "refx", "refy", "repeatcount", "repeatdur", "restart", "result", "rotate", "scale", "seed", "shape-rendering", "specularconstant", "specularexponent", "spreadmethod", "startoffset", "stddeviation", "stitchtiles", "stop-color", "stop-opacity", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke", "stroke-width", "style", "surfacescale", "systemlanguage", "tabindex", "targetx", "targety", "transform", "transform-origin", "text-anchor", "text-decoration", "text-rendering", "textlength", "type", "u1", "u2", "unicode", "values", "viewbox", "visibility", "version", "vert-adv-y", "vert-origin-x", "vert-origin-y", "width", "word-spacing", "wrap", "writing-mode", "xchannelselector", "ychannelselector", "x", "x1", "x2", "xmlns", "y", "y1", "y2", "z", "zoomandpan"]), $o = _e(["accent", "accentunder", "align", "bevelled", "close", "columnsalign", "columnlines", "columnspan", "denomalign", "depth", "dir", "display", "displaystyle", "encoding", "fence", "frame", "height", "href", "id", "largeop", "length", "linethickness", "lspace", "lquote", "mathbackground", "mathcolor", "mathsize", "mathvariant", "maxsize", "minsize", "movablelimits", "notation", "numalign", "open", "rowalign", "rowlines", "rowspacing", "rowspan", "rspace", "rquote", "scriptlevel", "scriptminsize", "scriptsizemultiplier", "selection", "separator", "separators", "stretchy", "subscriptshift", "supscriptshift", "symmetric", "voffset", "width", "xmlns"]), xn = _e(["xlink:href", "xml:id", "xlink:title", "xml:space", "xmlns:xlink"]), wu = Ue(/\{\{[\w\W]*|[\w\W]*\}\}/gm), ku = Ue(/<%[\w\W]*|[\w\W]*%>/gm), vu = Ue(/\${[\w\W]*}/gm), Eu = Ue(/^data-[\-\w.\u00B7-\uFFFF]/), yu = Ue(/^aria-[\-\w]+$/), na = Ue(
  /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i
  // eslint-disable-line no-useless-escape
), Tu = Ue(/^(?:\w+script|data):/i), Au = Ue(
  /[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g
  // eslint-disable-line no-control-regex
), la = Ue(/^html$/i), Su = Ue(/^[a-z][.\w]*(-[.\w]+)+$/i);
var er = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  MUSTACHE_EXPR: wu,
  ERB_EXPR: ku,
  TMPLIT_EXPR: vu,
  DATA_ATTR: Eu,
  ARIA_ATTR: yu,
  IS_ALLOWED_URI: na,
  IS_SCRIPT_OR_DATA: Tu,
  ATTR_WHITESPACE: Au,
  DOCTYPE_NAME: la,
  CUSTOM_ELEMENT: Su
});
const pn = {
  element: 1,
  attribute: 2,
  text: 3,
  cdataSection: 4,
  entityReference: 5,
  // Deprecated
  entityNode: 6,
  // Deprecated
  progressingInstruction: 7,
  comment: 8,
  document: 9,
  documentType: 10,
  documentFragment: 11,
  notation: 12
  // Deprecated
}, Cu = function() {
  return typeof window > "u" ? null : window;
}, Lu = function(e, t) {
  if (typeof e != "object" || typeof e.createPolicy != "function")
    return null;
  let n = null;
  const i = "data-tt-policy-suffix";
  t && t.hasAttribute(i) && (n = t.getAttribute(i));
  const o = "dompurify" + (n ? "#" + n : "");
  try {
    return e.createPolicy(o, {
      createHTML(s) {
        return s;
      },
      createScriptURL(s) {
        return s;
      }
    });
  } catch {
    return console.warn("TrustedTypes policy " + o + " could not be created."), null;
  }
};
function ia() {
  let l = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : Cu();
  const e = (R) => ia(R);
  if (e.version = "3.1.6", e.removed = [], !l || !l.document || l.document.nodeType !== pn.document)
    return e.isSupported = !1, e;
  let {
    document: t
  } = l;
  const n = t, i = n.currentScript, {
    DocumentFragment: o,
    HTMLTemplateElement: s,
    Node: f,
    Element: a,
    NodeFilter: r,
    NamedNodeMap: c = l.NamedNodeMap || l.MozNamedAttrMap,
    HTMLFormElement: u,
    DOMParser: _,
    trustedTypes: m
  } = l, p = a.prototype, y = bn(p, "cloneNode"), C = bn(p, "remove"), E = bn(p, "nextSibling"), b = bn(p, "childNodes"), v = bn(p, "parentNode");
  if (typeof s == "function") {
    const R = t.createElement("template");
    R.content && R.content.ownerDocument && (t = R.content.ownerDocument);
  }
  let g, S = "";
  const {
    implementation: w,
    createNodeIterator: L,
    createDocumentFragment: A,
    getElementsByTagName: q
  } = t, {
    importNode: F
  } = n;
  let P = {};
  e.isSupported = typeof ea == "function" && typeof v == "function" && w && w.createHTMLDocument !== void 0;
  const {
    MUSTACHE_EXPR: j,
    ERB_EXPR: de,
    TMPLIT_EXPR: x,
    DATA_ATTR: Ae,
    ARIA_ATTR: ee,
    IS_SCRIPT_OR_DATA: ke,
    ATTR_WHITESPACE: Se,
    CUSTOM_ELEMENT: re
  } = er;
  let {
    IS_ALLOWED_URI: G
  } = er, z = null;
  const Ze = O({}, [...Jo, ...Jl, ...Ql, ...xl, ...Qo]);
  let W = null;
  const wt = O({}, [...xo, ...$l, ...$o, ...xn]);
  let h = Object.seal(ta(null, {
    tagNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    attributeNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    allowCustomizedBuiltInElements: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: !1
    }
  })), me = null, $t = null, In = !0, en = !0, Rn = !1, Dn = !0, kt = !1, tn = !0, st = !1, nn = !1, ln = !1, vt = !1, Ut = !1, Ft = !1, Nn = !0, On = !1;
  const kl = "user-content-";
  let on = !0, k = !1, H = {}, te = null;
  const rn = O({}, ["annotation-xml", "audio", "colgroup", "desc", "foreignobject", "head", "iframe", "math", "mi", "mn", "mo", "ms", "mtext", "noembed", "noframes", "noscript", "plaintext", "script", "style", "svg", "template", "thead", "title", "video", "xmp"]);
  let zt = null;
  const vl = O({}, ["audio", "video", "img", "source", "image", "track"]);
  let Bt = null;
  const an = O({}, ["alt", "class", "for", "id", "label", "name", "pattern", "placeholder", "role", "summary", "title", "value", "style", "xmlns"]), Mn = "http://www.w3.org/1998/Math/MathML", Pn = "http://www.w3.org/2000/svg", ft = "http://www.w3.org/1999/xhtml";
  let qt = ft, El = !1, yl = null;
  const Ra = O({}, [Mn, Pn, ft], Kl);
  let sn = null;
  const Da = ["application/xhtml+xml", "text/html"], Na = "text/html";
  let $ = null, jt = null;
  const Oa = t.createElement("form"), Ui = function(d) {
    return d instanceof RegExp || d instanceof Function;
  }, Tl = function() {
    let d = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    if (!(jt && jt === d)) {
      if ((!d || typeof d != "object") && (d = {}), d = Ct(d), sn = // eslint-disable-next-line unicorn/prefer-includes
      Da.indexOf(d.PARSER_MEDIA_TYPE) === -1 ? Na : d.PARSER_MEDIA_TYPE, $ = sn === "application/xhtml+xml" ? Kl : nl, z = Ve(d, "ALLOWED_TAGS") ? O({}, d.ALLOWED_TAGS, $) : Ze, W = Ve(d, "ALLOWED_ATTR") ? O({}, d.ALLOWED_ATTR, $) : wt, yl = Ve(d, "ALLOWED_NAMESPACES") ? O({}, d.ALLOWED_NAMESPACES, Kl) : Ra, Bt = Ve(d, "ADD_URI_SAFE_ATTR") ? O(
        Ct(an),
        // eslint-disable-line indent
        d.ADD_URI_SAFE_ATTR,
        // eslint-disable-line indent
        $
        // eslint-disable-line indent
      ) : an, zt = Ve(d, "ADD_DATA_URI_TAGS") ? O(
        Ct(vl),
        // eslint-disable-line indent
        d.ADD_DATA_URI_TAGS,
        // eslint-disable-line indent
        $
        // eslint-disable-line indent
      ) : vl, te = Ve(d, "FORBID_CONTENTS") ? O({}, d.FORBID_CONTENTS, $) : rn, me = Ve(d, "FORBID_TAGS") ? O({}, d.FORBID_TAGS, $) : {}, $t = Ve(d, "FORBID_ATTR") ? O({}, d.FORBID_ATTR, $) : {}, H = Ve(d, "USE_PROFILES") ? d.USE_PROFILES : !1, In = d.ALLOW_ARIA_ATTR !== !1, en = d.ALLOW_DATA_ATTR !== !1, Rn = d.ALLOW_UNKNOWN_PROTOCOLS || !1, Dn = d.ALLOW_SELF_CLOSE_IN_ATTR !== !1, kt = d.SAFE_FOR_TEMPLATES || !1, tn = d.SAFE_FOR_XML !== !1, st = d.WHOLE_DOCUMENT || !1, vt = d.RETURN_DOM || !1, Ut = d.RETURN_DOM_FRAGMENT || !1, Ft = d.RETURN_TRUSTED_TYPE || !1, ln = d.FORCE_BODY || !1, Nn = d.SANITIZE_DOM !== !1, On = d.SANITIZE_NAMED_PROPS || !1, on = d.KEEP_CONTENT !== !1, k = d.IN_PLACE || !1, G = d.ALLOWED_URI_REGEXP || na, qt = d.NAMESPACE || ft, h = d.CUSTOM_ELEMENT_HANDLING || {}, d.CUSTOM_ELEMENT_HANDLING && Ui(d.CUSTOM_ELEMENT_HANDLING.tagNameCheck) && (h.tagNameCheck = d.CUSTOM_ELEMENT_HANDLING.tagNameCheck), d.CUSTOM_ELEMENT_HANDLING && Ui(d.CUSTOM_ELEMENT_HANDLING.attributeNameCheck) && (h.attributeNameCheck = d.CUSTOM_ELEMENT_HANDLING.attributeNameCheck), d.CUSTOM_ELEMENT_HANDLING && typeof d.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements == "boolean" && (h.allowCustomizedBuiltInElements = d.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements), kt && (en = !1), Ut && (vt = !0), H && (z = O({}, Qo), W = [], H.html === !0 && (O(z, Jo), O(W, xo)), H.svg === !0 && (O(z, Jl), O(W, $l), O(W, xn)), H.svgFilters === !0 && (O(z, Ql), O(W, $l), O(W, xn)), H.mathMl === !0 && (O(z, xl), O(W, $o), O(W, xn))), d.ADD_TAGS && (z === Ze && (z = Ct(z)), O(z, d.ADD_TAGS, $)), d.ADD_ATTR && (W === wt && (W = Ct(W)), O(W, d.ADD_ATTR, $)), d.ADD_URI_SAFE_ATTR && O(Bt, d.ADD_URI_SAFE_ATTR, $), d.FORBID_CONTENTS && (te === rn && (te = Ct(te)), O(te, d.FORBID_CONTENTS, $)), on && (z["#text"] = !0), st && O(z, ["html", "head", "body"]), z.table && (O(z, ["tbody"]), delete me.tbody), d.TRUSTED_TYPES_POLICY) {
        if (typeof d.TRUSTED_TYPES_POLICY.createHTML != "function")
          throw gn('TRUSTED_TYPES_POLICY configuration option must provide a "createHTML" hook.');
        if (typeof d.TRUSTED_TYPES_POLICY.createScriptURL != "function")
          throw gn('TRUSTED_TYPES_POLICY configuration option must provide a "createScriptURL" hook.');
        g = d.TRUSTED_TYPES_POLICY, S = g.createHTML("");
      } else
        g === void 0 && (g = Lu(m, i)), g !== null && typeof S == "string" && (S = g.createHTML(""));
      _e && _e(d), jt = d;
    }
  }, Fi = O({}, ["mi", "mo", "mn", "ms", "mtext"]), zi = O({}, ["foreignobject", "annotation-xml"]), Ma = O({}, ["title", "style", "font", "a", "script"]), Bi = O({}, [...Jl, ...Ql, ...bu]), qi = O({}, [...xl, ...pu]), Pa = function(d) {
    let T = v(d);
    (!T || !T.tagName) && (T = {
      namespaceURI: qt,
      tagName: "template"
    });
    const I = nl(d.tagName), V = nl(T.tagName);
    return yl[d.namespaceURI] ? d.namespaceURI === Pn ? T.namespaceURI === ft ? I === "svg" : T.namespaceURI === Mn ? I === "svg" && (V === "annotation-xml" || Fi[V]) : !!Bi[I] : d.namespaceURI === Mn ? T.namespaceURI === ft ? I === "math" : T.namespaceURI === Pn ? I === "math" && zi[V] : !!qi[I] : d.namespaceURI === ft ? T.namespaceURI === Pn && !zi[V] || T.namespaceURI === Mn && !Fi[V] ? !1 : !qi[I] && (Ma[I] || !Bi[I]) : !!(sn === "application/xhtml+xml" && yl[d.namespaceURI]) : !1;
  }, Ke = function(d) {
    mn(e.removed, {
      element: d
    });
    try {
      v(d).removeChild(d);
    } catch {
      C(d);
    }
  }, Un = function(d, T) {
    try {
      mn(e.removed, {
        attribute: T.getAttributeNode(d),
        from: T
      });
    } catch {
      mn(e.removed, {
        attribute: null,
        from: T
      });
    }
    if (T.removeAttribute(d), d === "is" && !W[d])
      if (vt || Ut)
        try {
          Ke(T);
        } catch {
        }
      else
        try {
          T.setAttribute(d, "");
        } catch {
        }
  }, ji = function(d) {
    let T = null, I = null;
    if (ln)
      d = "<remove></remove>" + d;
    else {
      const ne = Ko(d, /^[\r\n\t ]+/);
      I = ne && ne[0];
    }
    sn === "application/xhtml+xml" && qt === ft && (d = '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>' + d + "</body></html>");
    const V = g ? g.createHTML(d) : d;
    if (qt === ft)
      try {
        T = new _().parseFromString(V, sn);
      } catch {
      }
    if (!T || !T.documentElement) {
      T = w.createDocument(qt, "template", null);
      try {
        T.documentElement.innerHTML = El ? S : V;
      } catch {
      }
    }
    const ie = T.body || T.documentElement;
    return d && I && ie.insertBefore(t.createTextNode(I), ie.childNodes[0] || null), qt === ft ? q.call(T, st ? "html" : "body")[0] : st ? T.documentElement : ie;
  }, Hi = function(d) {
    return L.call(
      d.ownerDocument || d,
      d,
      // eslint-disable-next-line no-bitwise
      r.SHOW_ELEMENT | r.SHOW_COMMENT | r.SHOW_TEXT | r.SHOW_PROCESSING_INSTRUCTION | r.SHOW_CDATA_SECTION,
      null
    );
  }, Vi = function(d) {
    return d instanceof u && (typeof d.nodeName != "string" || typeof d.textContent != "string" || typeof d.removeChild != "function" || !(d.attributes instanceof c) || typeof d.removeAttribute != "function" || typeof d.setAttribute != "function" || typeof d.namespaceURI != "string" || typeof d.insertBefore != "function" || typeof d.hasChildNodes != "function");
  }, Wi = function(d) {
    return typeof f == "function" && d instanceof f;
  }, ct = function(d, T, I) {
    P[d] && Qn(P[d], (V) => {
      V.call(e, T, I, jt);
    });
  }, Gi = function(d) {
    let T = null;
    if (ct("beforeSanitizeElements", d, null), Vi(d))
      return Ke(d), !0;
    const I = $(d.nodeName);
    if (ct("uponSanitizeElement", d, {
      tagName: I,
      allowedTags: z
    }), d.hasChildNodes() && !Wi(d.firstElementChild) && fe(/<[/\w]/g, d.innerHTML) && fe(/<[/\w]/g, d.textContent) || d.nodeType === pn.progressingInstruction || tn && d.nodeType === pn.comment && fe(/<[/\w]/g, d.data))
      return Ke(d), !0;
    if (!z[I] || me[I]) {
      if (!me[I] && Xi(I) && (h.tagNameCheck instanceof RegExp && fe(h.tagNameCheck, I) || h.tagNameCheck instanceof Function && h.tagNameCheck(I)))
        return !1;
      if (on && !te[I]) {
        const V = v(d) || d.parentNode, ie = b(d) || d.childNodes;
        if (ie && V) {
          const ne = ie.length;
          for (let he = ne - 1; he >= 0; --he) {
            const Je = y(ie[he], !0);
            Je.__removalCount = (d.__removalCount || 0) + 1, V.insertBefore(Je, E(d));
          }
        }
      }
      return Ke(d), !0;
    }
    return d instanceof a && !Pa(d) || (I === "noscript" || I === "noembed" || I === "noframes") && fe(/<\/no(script|embed|frames)/i, d.innerHTML) ? (Ke(d), !0) : (kt && d.nodeType === pn.text && (T = d.textContent, Qn([j, de, x], (V) => {
      T = hn(T, V, " ");
    }), d.textContent !== T && (mn(e.removed, {
      element: d.cloneNode()
    }), d.textContent = T)), ct("afterSanitizeElements", d, null), !1);
  }, Yi = function(d, T, I) {
    if (Nn && (T === "id" || T === "name") && (I in t || I in Oa))
      return !1;
    if (!(en && !$t[T] && fe(Ae, T))) {
      if (!(In && fe(ee, T))) {
        if (!W[T] || $t[T]) {
          if (
            // First condition does a very basic check if a) it's basically a valid custom element tagname AND
            // b) if the tagName passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            // and c) if the attribute name passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.attributeNameCheck
            !(Xi(d) && (h.tagNameCheck instanceof RegExp && fe(h.tagNameCheck, d) || h.tagNameCheck instanceof Function && h.tagNameCheck(d)) && (h.attributeNameCheck instanceof RegExp && fe(h.attributeNameCheck, T) || h.attributeNameCheck instanceof Function && h.attributeNameCheck(T)) || // Alternative, second condition checks if it's an `is`-attribute, AND
            // the value passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            T === "is" && h.allowCustomizedBuiltInElements && (h.tagNameCheck instanceof RegExp && fe(h.tagNameCheck, I) || h.tagNameCheck instanceof Function && h.tagNameCheck(I)))
          ) return !1;
        } else if (!Bt[T]) {
          if (!fe(G, hn(I, Se, ""))) {
            if (!((T === "src" || T === "xlink:href" || T === "href") && d !== "script" && du(I, "data:") === 0 && zt[d])) {
              if (!(Rn && !fe(ke, hn(I, Se, "")))) {
                if (I)
                  return !1;
              }
            }
          }
        }
      }
    }
    return !0;
  }, Xi = function(d) {
    return d !== "annotation-xml" && Ko(d, re);
  }, Zi = function(d) {
    ct("beforeSanitizeAttributes", d, null);
    const {
      attributes: T
    } = d;
    if (!T)
      return;
    const I = {
      attrName: "",
      attrValue: "",
      keepAttr: !0,
      allowedAttributes: W
    };
    let V = T.length;
    for (; V--; ) {
      const ie = T[V], {
        name: ne,
        namespaceURI: he,
        value: Je
      } = ie, fn = $(ne);
      let ae = ne === "value" ? Je : mu(Je);
      if (I.attrName = fn, I.attrValue = ae, I.keepAttr = !0, I.forceKeepAttr = void 0, ct("uponSanitizeAttribute", d, I), ae = I.attrValue, tn && fe(/((--!?|])>)|<\/(style|title)/i, ae)) {
        Un(ne, d);
        continue;
      }
      if (I.forceKeepAttr || (Un(ne, d), !I.keepAttr))
        continue;
      if (!Dn && fe(/\/>/i, ae)) {
        Un(ne, d);
        continue;
      }
      kt && Qn([j, de, x], (Ji) => {
        ae = hn(ae, Ji, " ");
      });
      const Ki = $(d.nodeName);
      if (Yi(Ki, fn, ae)) {
        if (On && (fn === "id" || fn === "name") && (Un(ne, d), ae = kl + ae), g && typeof m == "object" && typeof m.getAttributeType == "function" && !he)
          switch (m.getAttributeType(Ki, fn)) {
            case "TrustedHTML": {
              ae = g.createHTML(ae);
              break;
            }
            case "TrustedScriptURL": {
              ae = g.createScriptURL(ae);
              break;
            }
          }
        try {
          he ? d.setAttributeNS(he, ne, ae) : d.setAttribute(ne, ae), Vi(d) ? Ke(d) : Zo(e.removed);
        } catch {
        }
      }
    }
    ct("afterSanitizeAttributes", d, null);
  }, Ua = function R(d) {
    let T = null;
    const I = Hi(d);
    for (ct("beforeSanitizeShadowDOM", d, null); T = I.nextNode(); )
      ct("uponSanitizeShadowNode", T, null), !Gi(T) && (T.content instanceof o && R(T.content), Zi(T));
    ct("afterSanitizeShadowDOM", d, null);
  };
  return e.sanitize = function(R) {
    let d = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}, T = null, I = null, V = null, ie = null;
    if (El = !R, El && (R = "<!-->"), typeof R != "string" && !Wi(R))
      if (typeof R.toString == "function") {
        if (R = R.toString(), typeof R != "string")
          throw gn("dirty is not a string, aborting");
      } else
        throw gn("toString is not a function");
    if (!e.isSupported)
      return R;
    if (nn || Tl(d), e.removed = [], typeof R == "string" && (k = !1), k) {
      if (R.nodeName) {
        const Je = $(R.nodeName);
        if (!z[Je] || me[Je])
          throw gn("root node is forbidden and cannot be sanitized in-place");
      }
    } else if (R instanceof f)
      T = ji("<!---->"), I = T.ownerDocument.importNode(R, !0), I.nodeType === pn.element && I.nodeName === "BODY" || I.nodeName === "HTML" ? T = I : T.appendChild(I);
    else {
      if (!vt && !kt && !st && // eslint-disable-next-line unicorn/prefer-includes
      R.indexOf("<") === -1)
        return g && Ft ? g.createHTML(R) : R;
      if (T = ji(R), !T)
        return vt ? null : Ft ? S : "";
    }
    T && ln && Ke(T.firstChild);
    const ne = Hi(k ? R : T);
    for (; V = ne.nextNode(); )
      Gi(V) || (V.content instanceof o && Ua(V.content), Zi(V));
    if (k)
      return R;
    if (vt) {
      if (Ut)
        for (ie = A.call(T.ownerDocument); T.firstChild; )
          ie.appendChild(T.firstChild);
      else
        ie = T;
      return (W.shadowroot || W.shadowrootmode) && (ie = F.call(n, ie, !0)), ie;
    }
    let he = st ? T.outerHTML : T.innerHTML;
    return st && z["!doctype"] && T.ownerDocument && T.ownerDocument.doctype && T.ownerDocument.doctype.name && fe(la, T.ownerDocument.doctype.name) && (he = "<!DOCTYPE " + T.ownerDocument.doctype.name + `>
` + he), kt && Qn([j, de, x], (Je) => {
      he = hn(he, Je, " ");
    }), g && Ft ? g.createHTML(he) : he;
  }, e.setConfig = function() {
    let R = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    Tl(R), nn = !0;
  }, e.clearConfig = function() {
    jt = null, nn = !1;
  }, e.isValidAttribute = function(R, d, T) {
    jt || Tl({});
    const I = $(R), V = $(d);
    return Yi(I, V, T);
  }, e.addHook = function(R, d) {
    typeof d == "function" && (P[R] = P[R] || [], mn(P[R], d));
  }, e.removeHook = function(R) {
    if (P[R])
      return Zo(P[R]);
  }, e.removeHooks = function(R) {
    P[R] && (P[R] = []);
  }, e.removeAllHooks = function() {
    P = {};
  }, e;
}
ia();
const {
  SvelteComponent: Iu,
  append_hydration: oa,
  attr: X,
  bubble: Ru,
  check_outros: Du,
  children: ra,
  claim_element: gl,
  claim_space: aa,
  create_slot: sa,
  detach: Ot,
  element: bl,
  empty: tr,
  get_all_dirty_from_scope: fa,
  get_slot_changes: ca,
  group_outros: Nu,
  init: Ou,
  insert_hydration: Tn,
  listen: Mu,
  safe_not_equal: Pu,
  set_style: we,
  space: ua,
  src_url_equal: rl,
  toggle_class: Zt,
  transition_in: al,
  transition_out: sl,
  update_slot_base: _a
} = window.__gradio__svelte__internal;
function Uu(l) {
  let e, t, n, i, o, s, f = (
    /*icon*/
    l[7] && nr(l)
  );
  const a = (
    /*#slots*/
    l[12].default
  ), r = sa(
    a,
    l,
    /*$$scope*/
    l[11],
    null
  );
  return {
    c() {
      e = bl("button"), f && f.c(), t = ua(), r && r.c(), this.h();
    },
    l(c) {
      e = gl(c, "BUTTON", {
        class: !0,
        id: !0
      });
      var u = ra(e);
      f && f.l(u), t = aa(u), r && r.l(u), u.forEach(Ot), this.h();
    },
    h() {
      X(e, "class", n = /*size*/
      l[4] + " " + /*variant*/
      l[3] + " " + /*elem_classes*/
      l[1].join(" ") + " svelte-8huxfn"), X(
        e,
        "id",
        /*elem_id*/
        l[0]
      ), e.disabled = /*disabled*/
      l[8], Zt(e, "hidden", !/*visible*/
      l[2]), we(
        e,
        "flex-grow",
        /*scale*/
        l[9]
      ), we(
        e,
        "width",
        /*scale*/
        l[9] === 0 ? "fit-content" : null
      ), we(e, "min-width", typeof /*min_width*/
      l[10] == "number" ? `calc(min(${/*min_width*/
      l[10]}px, 100%))` : null);
    },
    m(c, u) {
      Tn(c, e, u), f && f.m(e, null), oa(e, t), r && r.m(e, null), i = !0, o || (s = Mu(
        e,
        "click",
        /*click_handler*/
        l[13]
      ), o = !0);
    },
    p(c, u) {
      /*icon*/
      c[7] ? f ? f.p(c, u) : (f = nr(c), f.c(), f.m(e, t)) : f && (f.d(1), f = null), r && r.p && (!i || u & /*$$scope*/
      2048) && _a(
        r,
        a,
        c,
        /*$$scope*/
        c[11],
        i ? ca(
          a,
          /*$$scope*/
          c[11],
          u,
          null
        ) : fa(
          /*$$scope*/
          c[11]
        ),
        null
      ), (!i || u & /*size, variant, elem_classes*/
      26 && n !== (n = /*size*/
      c[4] + " " + /*variant*/
      c[3] + " " + /*elem_classes*/
      c[1].join(" ") + " svelte-8huxfn")) && X(e, "class", n), (!i || u & /*elem_id*/
      1) && X(
        e,
        "id",
        /*elem_id*/
        c[0]
      ), (!i || u & /*disabled*/
      256) && (e.disabled = /*disabled*/
      c[8]), (!i || u & /*size, variant, elem_classes, visible*/
      30) && Zt(e, "hidden", !/*visible*/
      c[2]), u & /*scale*/
      512 && we(
        e,
        "flex-grow",
        /*scale*/
        c[9]
      ), u & /*scale*/
      512 && we(
        e,
        "width",
        /*scale*/
        c[9] === 0 ? "fit-content" : null
      ), u & /*min_width*/
      1024 && we(e, "min-width", typeof /*min_width*/
      c[10] == "number" ? `calc(min(${/*min_width*/
      c[10]}px, 100%))` : null);
    },
    i(c) {
      i || (al(r, c), i = !0);
    },
    o(c) {
      sl(r, c), i = !1;
    },
    d(c) {
      c && Ot(e), f && f.d(), r && r.d(c), o = !1, s();
    }
  };
}
function Fu(l) {
  let e, t, n, i, o = (
    /*icon*/
    l[7] && lr(l)
  );
  const s = (
    /*#slots*/
    l[12].default
  ), f = sa(
    s,
    l,
    /*$$scope*/
    l[11],
    null
  );
  return {
    c() {
      e = bl("a"), o && o.c(), t = ua(), f && f.c(), this.h();
    },
    l(a) {
      e = gl(a, "A", {
        href: !0,
        rel: !0,
        "aria-disabled": !0,
        class: !0,
        id: !0
      });
      var r = ra(e);
      o && o.l(r), t = aa(r), f && f.l(r), r.forEach(Ot), this.h();
    },
    h() {
      X(
        e,
        "href",
        /*link*/
        l[6]
      ), X(e, "rel", "noopener noreferrer"), X(
        e,
        "aria-disabled",
        /*disabled*/
        l[8]
      ), X(e, "class", n = /*size*/
      l[4] + " " + /*variant*/
      l[3] + " " + /*elem_classes*/
      l[1].join(" ") + " svelte-8huxfn"), X(
        e,
        "id",
        /*elem_id*/
        l[0]
      ), Zt(e, "hidden", !/*visible*/
      l[2]), Zt(
        e,
        "disabled",
        /*disabled*/
        l[8]
      ), we(
        e,
        "flex-grow",
        /*scale*/
        l[9]
      ), we(
        e,
        "pointer-events",
        /*disabled*/
        l[8] ? "none" : null
      ), we(
        e,
        "width",
        /*scale*/
        l[9] === 0 ? "fit-content" : null
      ), we(e, "min-width", typeof /*min_width*/
      l[10] == "number" ? `calc(min(${/*min_width*/
      l[10]}px, 100%))` : null);
    },
    m(a, r) {
      Tn(a, e, r), o && o.m(e, null), oa(e, t), f && f.m(e, null), i = !0;
    },
    p(a, r) {
      /*icon*/
      a[7] ? o ? o.p(a, r) : (o = lr(a), o.c(), o.m(e, t)) : o && (o.d(1), o = null), f && f.p && (!i || r & /*$$scope*/
      2048) && _a(
        f,
        s,
        a,
        /*$$scope*/
        a[11],
        i ? ca(
          s,
          /*$$scope*/
          a[11],
          r,
          null
        ) : fa(
          /*$$scope*/
          a[11]
        ),
        null
      ), (!i || r & /*link*/
      64) && X(
        e,
        "href",
        /*link*/
        a[6]
      ), (!i || r & /*disabled*/
      256) && X(
        e,
        "aria-disabled",
        /*disabled*/
        a[8]
      ), (!i || r & /*size, variant, elem_classes*/
      26 && n !== (n = /*size*/
      a[4] + " " + /*variant*/
      a[3] + " " + /*elem_classes*/
      a[1].join(" ") + " svelte-8huxfn")) && X(e, "class", n), (!i || r & /*elem_id*/
      1) && X(
        e,
        "id",
        /*elem_id*/
        a[0]
      ), (!i || r & /*size, variant, elem_classes, visible*/
      30) && Zt(e, "hidden", !/*visible*/
      a[2]), (!i || r & /*size, variant, elem_classes, disabled*/
      282) && Zt(
        e,
        "disabled",
        /*disabled*/
        a[8]
      ), r & /*scale*/
      512 && we(
        e,
        "flex-grow",
        /*scale*/
        a[9]
      ), r & /*disabled*/
      256 && we(
        e,
        "pointer-events",
        /*disabled*/
        a[8] ? "none" : null
      ), r & /*scale*/
      512 && we(
        e,
        "width",
        /*scale*/
        a[9] === 0 ? "fit-content" : null
      ), r & /*min_width*/
      1024 && we(e, "min-width", typeof /*min_width*/
      a[10] == "number" ? `calc(min(${/*min_width*/
      a[10]}px, 100%))` : null);
    },
    i(a) {
      i || (al(f, a), i = !0);
    },
    o(a) {
      sl(f, a), i = !1;
    },
    d(a) {
      a && Ot(e), o && o.d(), f && f.d(a);
    }
  };
}
function nr(l) {
  let e, t, n;
  return {
    c() {
      e = bl("img"), this.h();
    },
    l(i) {
      e = gl(i, "IMG", {
        class: !0,
        src: !0,
        alt: !0
      }), this.h();
    },
    h() {
      X(e, "class", "button-icon svelte-8huxfn"), rl(e.src, t = /*icon*/
      l[7].url) || X(e, "src", t), X(e, "alt", n = `${/*value*/
      l[5]} icon`);
    },
    m(i, o) {
      Tn(i, e, o);
    },
    p(i, o) {
      o & /*icon*/
      128 && !rl(e.src, t = /*icon*/
      i[7].url) && X(e, "src", t), o & /*value*/
      32 && n !== (n = `${/*value*/
      i[5]} icon`) && X(e, "alt", n);
    },
    d(i) {
      i && Ot(e);
    }
  };
}
function lr(l) {
  let e, t, n;
  return {
    c() {
      e = bl("img"), this.h();
    },
    l(i) {
      e = gl(i, "IMG", {
        class: !0,
        src: !0,
        alt: !0
      }), this.h();
    },
    h() {
      X(e, "class", "button-icon svelte-8huxfn"), rl(e.src, t = /*icon*/
      l[7].url) || X(e, "src", t), X(e, "alt", n = `${/*value*/
      l[5]} icon`);
    },
    m(i, o) {
      Tn(i, e, o);
    },
    p(i, o) {
      o & /*icon*/
      128 && !rl(e.src, t = /*icon*/
      i[7].url) && X(e, "src", t), o & /*value*/
      32 && n !== (n = `${/*value*/
      i[5]} icon`) && X(e, "alt", n);
    },
    d(i) {
      i && Ot(e);
    }
  };
}
function zu(l) {
  let e, t, n, i;
  const o = [Fu, Uu], s = [];
  function f(a, r) {
    return (
      /*link*/
      a[6] && /*link*/
      a[6].length > 0 ? 0 : 1
    );
  }
  return e = f(l), t = s[e] = o[e](l), {
    c() {
      t.c(), n = tr();
    },
    l(a) {
      t.l(a), n = tr();
    },
    m(a, r) {
      s[e].m(a, r), Tn(a, n, r), i = !0;
    },
    p(a, [r]) {
      let c = e;
      e = f(a), e === c ? s[e].p(a, r) : (Nu(), sl(s[c], 1, 1, () => {
        s[c] = null;
      }), Du(), t = s[e], t ? t.p(a, r) : (t = s[e] = o[e](a), t.c()), al(t, 1), t.m(n.parentNode, n));
    },
    i(a) {
      i || (al(t), i = !0);
    },
    o(a) {
      sl(t), i = !1;
    },
    d(a) {
      a && Ot(n), s[e].d(a);
    }
  };
}
function Bu(l, e, t) {
  let {
    $$slots: n = {},
    $$scope: i
  } = e, {
    elem_id: o = ""
  } = e, {
    elem_classes: s = []
  } = e, {
    visible: f = !0
  } = e, {
    variant: a = "secondary"
  } = e, {
    size: r = "lg"
  } = e, {
    value: c = null
  } = e, {
    link: u = null
  } = e, {
    icon: _ = null
  } = e, {
    disabled: m = !1
  } = e, {
    scale: p = null
  } = e, {
    min_width: y = void 0
  } = e;
  function C(E) {
    Ru.call(this, l, E);
  }
  return l.$$set = (E) => {
    "elem_id" in E && t(0, o = E.elem_id), "elem_classes" in E && t(1, s = E.elem_classes), "visible" in E && t(2, f = E.visible), "variant" in E && t(3, a = E.variant), "size" in E && t(4, r = E.size), "value" in E && t(5, c = E.value), "link" in E && t(6, u = E.link), "icon" in E && t(7, _ = E.icon), "disabled" in E && t(8, m = E.disabled), "scale" in E && t(9, p = E.scale), "min_width" in E && t(10, y = E.min_width), "$$scope" in E && t(11, i = E.$$scope);
  }, [o, s, f, a, r, c, u, _, m, p, y, i, n, C];
}
class qu extends Iu {
  constructor(e) {
    super(), Ou(this, e, Bu, zu, Pu, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      variant: 3,
      size: 4,
      value: 5,
      link: 6,
      icon: 7,
      disabled: 8,
      scale: 9,
      min_width: 10
    });
  }
}
new Intl.Collator(0, {
  numeric: 1
}).compare;
class ei {
  constructor({
    path: e,
    url: t,
    orig_name: n,
    size: i,
    blob: o,
    is_stream: s,
    mime_type: f,
    alt_text: a,
    b64: r
  }) {
    Ce(this, "path");
    Ce(this, "url");
    Ce(this, "orig_name");
    Ce(this, "size");
    Ce(this, "blob");
    Ce(this, "is_stream");
    Ce(this, "mime_type");
    Ce(this, "alt_text");
    Ce(this, "b64");
    Ce(this, "meta", {
      _type: "gradio.FileData"
    });
    this.path = e, this.url = t, this.orig_name = n, this.size = i, this.blob = t ? void 0 : o, this.is_stream = s, this.mime_type = f, this.alt_text = a, this.b64 = r;
  }
}
typeof process < "u" && process.versions && process.versions.node;
var dt;
class qd extends TransformStream {
  /** Constructs a new instance. */
  constructor(t = {
    allowCR: !1
  }) {
    super({
      transform: (n, i) => {
        for (n = Ht(this, dt) + n; ; ) {
          const o = n.indexOf(`
`), s = t.allowCR ? n.indexOf("\r") : -1;
          if (s !== -1 && s !== n.length - 1 && (o === -1 || o - 1 > s)) {
            i.enqueue(n.slice(0, s)), n = n.slice(s + 1);
            continue;
          }
          if (o === -1) break;
          const f = n[o - 1] === "\r" ? o - 1 : o;
          i.enqueue(n.slice(0, f)), n = n.slice(o + 1);
        }
        eo(this, dt, n);
      },
      flush: (n) => {
        if (Ht(this, dt) === "") return;
        const i = t.allowCR && Ht(this, dt).endsWith("\r") ? Ht(this, dt).slice(0, -1) : Ht(this, dt);
        n.enqueue(i);
      }
    });
    $i(this, dt, "");
  }
}
dt = new WeakMap();
const {
  setContext: jd,
  getContext: ju
} = window.__gradio__svelte__internal, Hu = "WORKER_PROXY_CONTEXT_KEY";
function Vu() {
  return ju(Hu);
}
function Wu(l) {
  return l.host === window.location.host || l.host === "localhost:7860" || l.host === "127.0.0.1:7860" || // Ref: https://github.com/gradio-app/gradio/blob/v3.32.0/js/app/src/Index.svelte#L194
  l.host === "lite.local";
}
function Gu(l, e) {
  const t = e.toLowerCase();
  for (const [n, i] of Object.entries(l))
    if (n.toLowerCase() === t)
      return i;
}
function Yu(l) {
  if (l == null)
    return !1;
  const e = new URL(l, window.location.href);
  return !(!Wu(e) || e.protocol !== "http:" && e.protocol !== "https:");
}
const {
  SvelteComponent: Xu,
  assign: fl,
  check_outros: da,
  children: ma,
  claim_element: ha,
  compute_rest_props: ir,
  create_slot: Li,
  detach: xt,
  element: ga,
  empty: cl,
  exclude_internal_props: Zu,
  get_all_dirty_from_scope: Ii,
  get_slot_changes: Ri,
  get_spread_update: ba,
  group_outros: pa,
  init: Ku,
  insert_hydration: pl,
  listen: wa,
  prevent_default: Ju,
  safe_not_equal: Qu,
  set_attributes: ul,
  transition_in: Mt,
  transition_out: Pt,
  update_slot_base: Di
} = window.__gradio__svelte__internal, {
  createEventDispatcher: xu
} = window.__gradio__svelte__internal;
function $u(l) {
  let e, t, n, i, o;
  const s = (
    /*#slots*/
    l[8].default
  ), f = Li(
    s,
    l,
    /*$$scope*/
    l[7],
    null
  );
  let a = [
    {
      href: (
        /*href*/
        l[0]
      )
    },
    {
      target: t = typeof window < "u" && window.__is_colab__ ? "_blank" : null
    },
    {
      rel: "noopener noreferrer"
    },
    {
      download: (
        /*download*/
        l[1]
      )
    },
    /*$$restProps*/
    l[6]
  ], r = {};
  for (let c = 0; c < a.length; c += 1)
    r = fl(r, a[c]);
  return {
    c() {
      e = ga("a"), f && f.c(), this.h();
    },
    l(c) {
      e = ha(c, "A", {
        href: !0,
        target: !0,
        rel: !0,
        download: !0
      });
      var u = ma(e);
      f && f.l(u), u.forEach(xt), this.h();
    },
    h() {
      ul(e, r);
    },
    m(c, u) {
      pl(c, e, u), f && f.m(e, null), n = !0, i || (o = wa(
        e,
        "click",
        /*dispatch*/
        l[3].bind(null, "click")
      ), i = !0);
    },
    p(c, u) {
      f && f.p && (!n || u & /*$$scope*/
      128) && Di(
        f,
        s,
        c,
        /*$$scope*/
        c[7],
        n ? Ri(
          s,
          /*$$scope*/
          c[7],
          u,
          null
        ) : Ii(
          /*$$scope*/
          c[7]
        ),
        null
      ), ul(e, r = ba(a, [(!n || u & /*href*/
      1) && {
        href: (
          /*href*/
          c[0]
        )
      }, {
        target: t
      }, {
        rel: "noopener noreferrer"
      }, (!n || u & /*download*/
      2) && {
        download: (
          /*download*/
          c[1]
        )
      }, u & /*$$restProps*/
      64 && /*$$restProps*/
      c[6]]));
    },
    i(c) {
      n || (Mt(f, c), n = !0);
    },
    o(c) {
      Pt(f, c), n = !1;
    },
    d(c) {
      c && xt(e), f && f.d(c), i = !1, o();
    }
  };
}
function e_(l) {
  let e, t, n, i;
  const o = [n_, t_], s = [];
  function f(a, r) {
    return (
      /*is_downloading*/
      a[2] ? 0 : 1
    );
  }
  return e = f(l), t = s[e] = o[e](l), {
    c() {
      t.c(), n = cl();
    },
    l(a) {
      t.l(a), n = cl();
    },
    m(a, r) {
      s[e].m(a, r), pl(a, n, r), i = !0;
    },
    p(a, r) {
      let c = e;
      e = f(a), e === c ? s[e].p(a, r) : (pa(), Pt(s[c], 1, 1, () => {
        s[c] = null;
      }), da(), t = s[e], t ? t.p(a, r) : (t = s[e] = o[e](a), t.c()), Mt(t, 1), t.m(n.parentNode, n));
    },
    i(a) {
      i || (Mt(t), i = !0);
    },
    o(a) {
      Pt(t), i = !1;
    },
    d(a) {
      a && xt(n), s[e].d(a);
    }
  };
}
function t_(l) {
  let e, t, n, i;
  const o = (
    /*#slots*/
    l[8].default
  ), s = Li(
    o,
    l,
    /*$$scope*/
    l[7],
    null
  );
  let f = [
    /*$$restProps*/
    l[6],
    {
      href: (
        /*href*/
        l[0]
      )
    }
  ], a = {};
  for (let r = 0; r < f.length; r += 1)
    a = fl(a, f[r]);
  return {
    c() {
      e = ga("a"), s && s.c(), this.h();
    },
    l(r) {
      e = ha(r, "A", {
        href: !0
      });
      var c = ma(e);
      s && s.l(c), c.forEach(xt), this.h();
    },
    h() {
      ul(e, a);
    },
    m(r, c) {
      pl(r, e, c), s && s.m(e, null), t = !0, n || (i = wa(e, "click", Ju(
        /*wasm_click_handler*/
        l[5]
      )), n = !0);
    },
    p(r, c) {
      s && s.p && (!t || c & /*$$scope*/
      128) && Di(
        s,
        o,
        r,
        /*$$scope*/
        r[7],
        t ? Ri(
          o,
          /*$$scope*/
          r[7],
          c,
          null
        ) : Ii(
          /*$$scope*/
          r[7]
        ),
        null
      ), ul(e, a = ba(f, [c & /*$$restProps*/
      64 && /*$$restProps*/
      r[6], (!t || c & /*href*/
      1) && {
        href: (
          /*href*/
          r[0]
        )
      }]));
    },
    i(r) {
      t || (Mt(s, r), t = !0);
    },
    o(r) {
      Pt(s, r), t = !1;
    },
    d(r) {
      r && xt(e), s && s.d(r), n = !1, i();
    }
  };
}
function n_(l) {
  let e;
  const t = (
    /*#slots*/
    l[8].default
  ), n = Li(
    t,
    l,
    /*$$scope*/
    l[7],
    null
  );
  return {
    c() {
      n && n.c();
    },
    l(i) {
      n && n.l(i);
    },
    m(i, o) {
      n && n.m(i, o), e = !0;
    },
    p(i, o) {
      n && n.p && (!e || o & /*$$scope*/
      128) && Di(
        n,
        t,
        i,
        /*$$scope*/
        i[7],
        e ? Ri(
          t,
          /*$$scope*/
          i[7],
          o,
          null
        ) : Ii(
          /*$$scope*/
          i[7]
        ),
        null
      );
    },
    i(i) {
      e || (Mt(n, i), e = !0);
    },
    o(i) {
      Pt(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function l_(l) {
  let e, t, n, i, o;
  const s = [e_, $u], f = [];
  function a(r, c) {
    return c & /*href*/
    1 && (e = null), e == null && (e = !!/*worker_proxy*/
    (r[4] && Yu(
      /*href*/
      r[0]
    ))), e ? 0 : 1;
  }
  return t = a(l, -1), n = f[t] = s[t](l), {
    c() {
      n.c(), i = cl();
    },
    l(r) {
      n.l(r), i = cl();
    },
    m(r, c) {
      f[t].m(r, c), pl(r, i, c), o = !0;
    },
    p(r, [c]) {
      let u = t;
      t = a(r, c), t === u ? f[t].p(r, c) : (pa(), Pt(f[u], 1, 1, () => {
        f[u] = null;
      }), da(), n = f[t], n ? n.p(r, c) : (n = f[t] = s[t](r), n.c()), Mt(n, 1), n.m(i.parentNode, i));
    },
    i(r) {
      o || (Mt(n), o = !0);
    },
    o(r) {
      Pt(n), o = !1;
    },
    d(r) {
      r && xt(i), f[t].d(r);
    }
  };
}
function i_(l, e, t) {
  const n = ["href", "download"];
  let i = ir(e, n), {
    $$slots: o = {},
    $$scope: s
  } = e;
  var f = this && this.__awaiter || function(p, y, C, E) {
    function b(v) {
      return v instanceof C ? v : new C(function(g) {
        g(v);
      });
    }
    return new (C || (C = Promise))(function(v, g) {
      function S(A) {
        try {
          L(E.next(A));
        } catch (q) {
          g(q);
        }
      }
      function w(A) {
        try {
          L(E.throw(A));
        } catch (q) {
          g(q);
        }
      }
      function L(A) {
        A.done ? v(A.value) : b(A.value).then(S, w);
      }
      L((E = E.apply(p, y || [])).next());
    });
  };
  let {
    href: a = void 0
  } = e, {
    download: r
  } = e;
  const c = xu();
  let u = !1;
  const _ = Vu();
  function m() {
    return f(this, void 0, void 0, function* () {
      if (u)
        return;
      if (c("click"), a == null)
        throw new Error("href is not defined.");
      if (_ == null)
        throw new Error("Wasm worker proxy is not available.");
      const y = new URL(a, window.location.href).pathname;
      t(2, u = !0), _.httpRequest({
        method: "GET",
        path: y,
        headers: {},
        query_string: ""
      }).then((C) => {
        if (C.status !== 200)
          throw new Error(`Failed to get file ${y} from the Wasm worker.`);
        const E = new Blob([C.body], {
          type: Gu(C.headers, "content-type")
        }), b = URL.createObjectURL(E), v = document.createElement("a");
        v.href = b, v.download = r, v.click(), URL.revokeObjectURL(b);
      }).finally(() => {
        t(2, u = !1);
      });
    });
  }
  return l.$$set = (p) => {
    e = fl(fl({}, e), Zu(p)), t(6, i = ir(e, n)), "href" in p && t(0, a = p.href), "download" in p && t(1, r = p.download), "$$scope" in p && t(7, s = p.$$scope);
  }, [a, r, u, c, _, m, i, s, o];
}
class o_ extends Xu {
  constructor(e) {
    super(), Ku(this, e, i_, l_, Qu, {
      href: 0,
      download: 1
    });
  }
}
const {
  SvelteComponent: r_,
  append_hydration: ti,
  attr: a_,
  check_outros: ni,
  children: s_,
  claim_component: An,
  claim_element: f_,
  claim_space: li,
  create_component: Sn,
  destroy_component: Cn,
  detach: or,
  element: c_,
  group_outros: ii,
  init: u_,
  insert_hydration: __,
  mount_component: Ln,
  safe_not_equal: d_,
  set_style: rr,
  space: oi,
  toggle_class: ar,
  transition_in: pe,
  transition_out: We
} = window.__gradio__svelte__internal, {
  createEventDispatcher: m_
} = window.__gradio__svelte__internal;
function sr(l) {
  let e, t;
  return e = new St({
    props: {
      Icon: Af,
      label: (
        /*i18n*/
        l[4]("common.edit")
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    l[6]
  ), {
    c() {
      Sn(e.$$.fragment);
    },
    l(n) {
      An(e.$$.fragment, n);
    },
    m(n, i) {
      Ln(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      n[4]("common.edit")), e.$set(o);
    },
    i(n) {
      t || (pe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      We(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Cn(e, n);
    }
  };
}
function fr(l) {
  let e, t;
  return e = new St({
    props: {
      Icon: Vf,
      label: (
        /*i18n*/
        l[4]("common.undo")
      )
    }
  }), e.$on(
    "click",
    /*click_handler_1*/
    l[7]
  ), {
    c() {
      Sn(e.$$.fragment);
    },
    l(n) {
      An(e.$$.fragment, n);
    },
    m(n, i) {
      Ln(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      n[4]("common.undo")), e.$set(o);
    },
    i(n) {
      t || (pe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      We(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Cn(e, n);
    }
  };
}
function cr(l) {
  let e, t;
  return e = new o_({
    props: {
      href: (
        /*download*/
        l[2]
      ),
      download: !0,
      $$slots: {
        default: [h_]
      },
      $$scope: {
        ctx: l
      }
    }
  }), {
    c() {
      Sn(e.$$.fragment);
    },
    l(n) {
      An(e.$$.fragment, n);
    },
    m(n, i) {
      Ln(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*download*/
      4 && (o.href = /*download*/
      n[2]), i & /*$$scope, i18n*/
      528 && (o.$$scope = {
        dirty: i,
        ctx: n
      }), e.$set(o);
    },
    i(n) {
      t || (pe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      We(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Cn(e, n);
    }
  };
}
function h_(l) {
  let e, t;
  return e = new St({
    props: {
      Icon: zr,
      label: (
        /*i18n*/
        l[4]("common.download")
      )
    }
  }), {
    c() {
      Sn(e.$$.fragment);
    },
    l(n) {
      An(e.$$.fragment, n);
    },
    m(n, i) {
      Ln(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      n[4]("common.download")), e.$set(o);
    },
    i(n) {
      t || (pe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      We(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Cn(e, n);
    }
  };
}
function g_(l) {
  let e, t, n, i, o, s, f = (
    /*editable*/
    l[0] && sr(l)
  ), a = (
    /*undoable*/
    l[1] && fr(l)
  ), r = (
    /*download*/
    l[2] && cr(l)
  );
  return o = new St({
    props: {
      Icon: of,
      label: (
        /*i18n*/
        l[4]("common.clear")
      )
    }
  }), o.$on(
    "click",
    /*click_handler_2*/
    l[8]
  ), {
    c() {
      e = c_("div"), f && f.c(), t = oi(), a && a.c(), n = oi(), r && r.c(), i = oi(), Sn(o.$$.fragment), this.h();
    },
    l(c) {
      e = f_(c, "DIV", {
        class: !0
      });
      var u = s_(e);
      f && f.l(u), t = li(u), a && a.l(u), n = li(u), r && r.l(u), i = li(u), An(o.$$.fragment, u), u.forEach(or), this.h();
    },
    h() {
      a_(e, "class", "svelte-1wj0ocy"), ar(e, "not-absolute", !/*absolute*/
      l[3]), rr(
        e,
        "position",
        /*absolute*/
        l[3] ? "absolute" : "static"
      );
    },
    m(c, u) {
      __(c, e, u), f && f.m(e, null), ti(e, t), a && a.m(e, null), ti(e, n), r && r.m(e, null), ti(e, i), Ln(o, e, null), s = !0;
    },
    p(c, [u]) {
      /*editable*/
      c[0] ? f ? (f.p(c, u), u & /*editable*/
      1 && pe(f, 1)) : (f = sr(c), f.c(), pe(f, 1), f.m(e, t)) : f && (ii(), We(f, 1, 1, () => {
        f = null;
      }), ni()), /*undoable*/
      c[1] ? a ? (a.p(c, u), u & /*undoable*/
      2 && pe(a, 1)) : (a = fr(c), a.c(), pe(a, 1), a.m(e, n)) : a && (ii(), We(a, 1, 1, () => {
        a = null;
      }), ni()), /*download*/
      c[2] ? r ? (r.p(c, u), u & /*download*/
      4 && pe(r, 1)) : (r = cr(c), r.c(), pe(r, 1), r.m(e, i)) : r && (ii(), We(r, 1, 1, () => {
        r = null;
      }), ni());
      const _ = {};
      u & /*i18n*/
      16 && (_.label = /*i18n*/
      c[4]("common.clear")), o.$set(_), (!s || u & /*absolute*/
      8) && ar(e, "not-absolute", !/*absolute*/
      c[3]), u & /*absolute*/
      8 && rr(
        e,
        "position",
        /*absolute*/
        c[3] ? "absolute" : "static"
      );
    },
    i(c) {
      s || (pe(f), pe(a), pe(r), pe(o.$$.fragment, c), s = !0);
    },
    o(c) {
      We(f), We(a), We(r), We(o.$$.fragment, c), s = !1;
    },
    d(c) {
      c && or(e), f && f.d(), a && a.d(), r && r.d(), Cn(o);
    }
  };
}
function b_(l, e, t) {
  let {
    editable: n = !1
  } = e, {
    undoable: i = !1
  } = e, {
    download: o = null
  } = e, {
    absolute: s = !0
  } = e, {
    i18n: f
  } = e;
  const a = m_(), r = () => a("edit"), c = () => a("undo"), u = (_) => {
    a("clear"), _.stopPropagation();
  };
  return l.$$set = (_) => {
    "editable" in _ && t(0, n = _.editable), "undoable" in _ && t(1, i = _.undoable), "download" in _ && t(2, o = _.download), "absolute" in _ && t(3, s = _.absolute), "i18n" in _ && t(4, f = _.i18n);
  }, [n, i, o, s, f, a, r, c, u];
}
class p_ extends r_ {
  constructor(e) {
    super(), u_(this, e, b_, g_, d_, {
      editable: 0,
      undoable: 1,
      download: 2,
      absolute: 3,
      i18n: 4
    });
  }
}
function ka(l, e, t) {
  if (l == null)
    return null;
  if (Array.isArray(l)) {
    const n = [];
    for (const i of l)
      i == null ? n.push(null) : n.push(ka(i, e, t));
    return n;
  }
  return l.is_stream ? t == null ? new ei({
    ...l,
    url: e + "/stream/" + l.path
  }) : new ei({
    ...l,
    url: "/proxy=" + t + "stream/" + l.path
  }) : new ei({
    ...l,
    url: E_(l.path, e, t)
  });
}
function w_(l) {
  try {
    const e = new URL(l);
    return e.protocol === "http:" || e.protocol === "https:";
  } catch {
    return !1;
  }
}
function k_() {
  const l = document.querySelector(".gradio-container");
  if (!l)
    return "";
  const e = l.className.match(/gradio-container-(.+)/);
  return e ? e[1] : "";
}
const v_ = +k_()[0];
function E_(l, e, t) {
  const n = v_ >= 5 ? "gradio_api/" : "";
  return l == null ? t ? `/proxy=${t}${n}file=` : `${e}${n}file=` : w_(l) ? l : t ? `/proxy=${t}${n}file=${l}` : `${e}/${n}file=${l}`;
}
var ur = Object.prototype.hasOwnProperty;
function _r(l, e, t) {
  for (t of l.keys())
    if (vn(t, e)) return t;
}
function vn(l, e) {
  var t, n, i;
  if (l === e) return !0;
  if (l && e && (t = l.constructor) === e.constructor) {
    if (t === Date) return l.getTime() === e.getTime();
    if (t === RegExp) return l.toString() === e.toString();
    if (t === Array) {
      if ((n = l.length) === e.length)
        for (; n-- && vn(l[n], e[n]); ) ;
      return n === -1;
    }
    if (t === Set) {
      if (l.size !== e.size)
        return !1;
      for (n of l)
        if (i = n, i && typeof i == "object" && (i = _r(e, i), !i) || !e.has(i)) return !1;
      return !0;
    }
    if (t === Map) {
      if (l.size !== e.size)
        return !1;
      for (n of l)
        if (i = n[0], i && typeof i == "object" && (i = _r(e, i), !i) || !vn(n[1], e.get(i)))
          return !1;
      return !0;
    }
    if (t === ArrayBuffer)
      l = new Uint8Array(l), e = new Uint8Array(e);
    else if (t === DataView) {
      if ((n = l.byteLength) === e.byteLength)
        for (; n-- && l.getInt8(n) === e.getInt8(n); ) ;
      return n === -1;
    }
    if (ArrayBuffer.isView(l)) {
      if ((n = l.byteLength) === e.byteLength)
        for (; n-- && l[n] === e[n]; ) ;
      return n === -1;
    }
    if (!t || typeof l == "object") {
      n = 0;
      for (t in l)
        if (ur.call(l, t) && ++n && !ur.call(e, t) || !(t in e) || !vn(l[t], e[t])) return !1;
      return Object.keys(e).length === n;
    }
  }
  return l !== l && e !== e;
}
const {
  SvelteComponent: y_,
  append_hydration: dr,
  attr: oe,
  children: ri,
  claim_svg_element: ai,
  detach: $n,
  init: T_,
  insert_hydration: A_,
  noop: mr,
  safe_not_equal: S_,
  svg_element: si
} = window.__gradio__svelte__internal;
function C_(l) {
  let e, t, n, i;
  return {
    c() {
      e = si("svg"), t = si("path"), n = si("path"), this.h();
    },
    l(o) {
      e = ai(o, "svg", {
        xmlns: !0,
        viewBox: !0,
        fill: !0,
        "stroke-width": !0,
        color: !0,
        transform: !0
      });
      var s = ri(e);
      t = ai(s, "path", {
        stroke: !0,
        "stroke-width": !0,
        "stroke-linecap": !0,
        d: !0
      }), ri(t).forEach($n), n = ai(s, "path", {
        stroke: !0,
        "stroke-width": !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0,
        d: !0
      }), ri(n).forEach($n), s.forEach($n), this.h();
    },
    h() {
      oe(t, "stroke", "currentColor"), oe(t, "stroke-width", "1.5"), oe(t, "stroke-linecap", "round"), oe(t, "d", "M16.472 20H4.1a.6.6 0 0 1-.6-.6V9.6a.6.6 0 0 1 .6-.6h2.768a2 2 0 0 0 1.715-.971l2.71-4.517a1.631 1.631 0 0 1 2.961 1.308l-1.022 3.408a.6.6 0 0 0 .574.772h4.575a2 2 0 0 1 1.93 2.526l-1.91 7A2 2 0 0 1 16.473 20Z"), oe(n, "stroke", "currentColor"), oe(n, "stroke-width", "1.5"), oe(n, "stroke-linecap", "round"), oe(n, "stroke-linejoin", "round"), oe(n, "d", "M7 20V9"), oe(e, "xmlns", "http://www.w3.org/2000/svg"), oe(e, "viewBox", "0 0 24 24"), oe(e, "fill", i = /*selected*/
      l[0] ? "currentColor" : "none"), oe(e, "stroke-width", "1.5"), oe(e, "color", "currentColor"), oe(e, "transform", "rotate(180)");
    },
    m(o, s) {
      A_(o, e, s), dr(e, t), dr(e, n);
    },
    p(o, [s]) {
      s & /*selected*/
      1 && i !== (i = /*selected*/
      o[0] ? "currentColor" : "none") && oe(e, "fill", i);
    },
    i: mr,
    o: mr,
    d(o) {
      o && $n(e);
    }
  };
}
function L_(l, e, t) {
  let {
    selected: n
  } = e;
  return l.$$set = (i) => {
    "selected" in i && t(0, n = i.selected);
  }, [n];
}
class I_ extends y_ {
  constructor(e) {
    super(), T_(this, e, L_, C_, S_, {
      selected: 0
    });
  }
}
const {
  SvelteComponent: R_,
  append_hydration: mt,
  attr: et,
  check_outros: D_,
  children: Qt,
  claim_component: hr,
  claim_element: Dt,
  claim_space: ll,
  claim_text: va,
  create_component: gr,
  destroy_component: br,
  detach: ot,
  element: Nt,
  flush: el,
  group_outros: N_,
  init: O_,
  insert_hydration: wl,
  listen: Ea,
  mount_component: pr,
  safe_not_equal: M_,
  set_data: ya,
  set_style: P_,
  space: il,
  src_url_equal: wr,
  text: Ta,
  transition_in: En,
  transition_out: _l
} = window.__gradio__svelte__internal, {
  createEventDispatcher: U_
} = window.__gradio__svelte__internal;
function kr(l) {
  let e, t = (
    /*value*/
    l[0].caption + ""
  ), n;
  return {
    c() {
      e = Nt("div"), n = Ta(t), this.h();
    },
    l(i) {
      e = Dt(i, "DIV", {
        class: !0
      });
      var o = Qt(e);
      n = va(o, t), o.forEach(ot), this.h();
    },
    h() {
      et(e, "class", "foot-label left-label svelte-u350v8");
    },
    m(i, o) {
      wl(i, e, o), mt(e, n);
    },
    p(i, o) {
      o & /*value*/
      1 && t !== (t = /*value*/
      i[0].caption + "") && ya(n, t);
    },
    d(i) {
      i && ot(e);
    }
  };
}
function vr(l) {
  let e, t, n, i;
  return {
    c() {
      e = Nt("button"), t = Ta(
        /*action_label*/
        l[3]
      ), this.h();
    },
    l(o) {
      e = Dt(o, "BUTTON", {
        class: !0
      });
      var s = Qt(e);
      t = va(
        s,
        /*action_label*/
        l[3]
      ), s.forEach(ot), this.h();
    },
    h() {
      et(e, "class", "foot-label right-label svelte-u350v8");
    },
    m(o, s) {
      wl(o, e, s), mt(e, t), n || (i = Ea(
        e,
        "click",
        /*click_handler_1*/
        l[6]
      ), n = !0);
    },
    p(o, s) {
      s & /*action_label*/
      8 && ya(
        t,
        /*action_label*/
        o[3]
      );
    },
    d(o) {
      o && ot(e), n = !1, i();
    }
  };
}
function Er(l) {
  let e, t, n, i, o, s, f;
  return n = new St({
    props: {
      size: "large",
      highlight: (
        /*value*/
        l[0].liked
      ),
      Icon: Ff
    }
  }), n.$on(
    "click",
    /*click_handler_2*/
    l[7]
  ), s = new St({
    props: {
      size: "large",
      highlight: (
        /*value*/
        l[0].liked === !1
      ),
      Icon: I_
    }
  }), s.$on(
    "click",
    /*click_handler_3*/
    l[8]
  ), {
    c() {
      e = Nt("div"), t = Nt("span"), gr(n.$$.fragment), i = il(), o = Nt("span"), gr(s.$$.fragment), this.h();
    },
    l(a) {
      e = Dt(a, "DIV", {
        class: !0
      });
      var r = Qt(e);
      t = Dt(r, "SPAN", {
        style: !0
      });
      var c = Qt(t);
      hr(n.$$.fragment, c), c.forEach(ot), i = ll(r), o = Dt(r, "SPAN", {});
      var u = Qt(o);
      hr(s.$$.fragment, u), u.forEach(ot), r.forEach(ot), this.h();
    },
    h() {
      P_(t, "margin-right", "1px"), et(e, "class", "like-button svelte-u350v8");
    },
    m(a, r) {
      wl(a, e, r), mt(e, t), pr(n, t, null), mt(e, i), mt(e, o), pr(s, o, null), f = !0;
    },
    p(a, r) {
      const c = {};
      r & /*value*/
      1 && (c.highlight = /*value*/
      a[0].liked), n.$set(c);
      const u = {};
      r & /*value*/
      1 && (u.highlight = /*value*/
      a[0].liked === !1), s.$set(u);
    },
    i(a) {
      f || (En(n.$$.fragment, a), En(s.$$.fragment, a), f = !0);
    },
    o(a) {
      _l(n.$$.fragment, a), _l(s.$$.fragment, a), f = !1;
    },
    d(a) {
      a && ot(e), br(n), br(s);
    }
  };
}
function F_(l) {
  let e, t, n, i, o, s, f, a, r, c, u = (
    /*value*/
    l[0].caption && kr(l)
  ), _ = (
    /*clickable*/
    l[2] && vr(l)
  ), m = (
    /*likeable*/
    l[1] && Er(l)
  );
  return {
    c() {
      e = Nt("div"), t = Nt("img"), o = il(), u && u.c(), s = il(), _ && _.c(), f = il(), m && m.c(), this.h();
    },
    l(p) {
      e = Dt(p, "DIV", {
        class: !0
      });
      var y = Qt(e);
      t = Dt(y, "IMG", {
        alt: !0,
        src: !0,
        class: !0,
        loading: !0
      }), o = ll(y), u && u.l(y), s = ll(y), _ && _.l(y), f = ll(y), m && m.l(y), y.forEach(ot), this.h();
    },
    h() {
      et(t, "alt", n = /*value*/
      l[0].caption || ""), wr(t.src, i = /*value*/
      l[0].image.url) || et(t, "src", i), et(t, "class", "thumbnail-img svelte-u350v8"), et(t, "loading", "lazy"), et(e, "class", "thumbnail-image-box svelte-u350v8");
    },
    m(p, y) {
      wl(p, e, y), mt(e, t), mt(e, o), u && u.m(e, null), mt(e, s), _ && _.m(e, null), mt(e, f), m && m.m(e, null), a = !0, r || (c = Ea(
        t,
        "click",
        /*click_handler*/
        l[5]
      ), r = !0);
    },
    p(p, [y]) {
      (!a || y & /*value*/
      1 && n !== (n = /*value*/
      p[0].caption || "")) && et(t, "alt", n), (!a || y & /*value*/
      1 && !wr(t.src, i = /*value*/
      p[0].image.url)) && et(t, "src", i), /*value*/
      p[0].caption ? u ? u.p(p, y) : (u = kr(p), u.c(), u.m(e, s)) : u && (u.d(1), u = null), /*clickable*/
      p[2] ? _ ? _.p(p, y) : (_ = vr(p), _.c(), _.m(e, f)) : _ && (_.d(1), _ = null), /*likeable*/
      p[1] ? m ? (m.p(p, y), y & /*likeable*/
      2 && En(m, 1)) : (m = Er(p), m.c(), En(m, 1), m.m(e, null)) : m && (N_(), _l(m, 1, 1, () => {
        m = null;
      }), D_());
    },
    i(p) {
      a || (En(m), a = !0);
    },
    o(p) {
      _l(m), a = !1;
    },
    d(p) {
      p && ot(e), u && u.d(), _ && _.d(), m && m.d(), r = !1, c();
    }
  };
}
function z_(l, e, t) {
  const n = U_();
  let {
    likeable: i
  } = e, {
    clickable: o
  } = e, {
    value: s
  } = e, {
    action_label: f
  } = e;
  const a = () => n("click"), r = () => {
    n("label_click");
  }, c = () => {
    if (s.liked) {
      t(0, s.liked = void 0, s), n("like", void 0);
      return;
    }
    t(0, s.liked = !0, s), n("like", !0);
  }, u = () => {
    if (s.liked === !1) {
      t(0, s.liked = void 0, s), n("like", void 0);
      return;
    }
    t(0, s.liked = !1, s), n("like", !1);
  };
  return l.$$set = (_) => {
    "likeable" in _ && t(1, i = _.likeable), "clickable" in _ && t(2, o = _.clickable), "value" in _ && t(0, s = _.value), "action_label" in _ && t(3, f = _.action_label);
  }, [s, i, o, f, n, a, r, c, u];
}
class B_ extends R_ {
  constructor(e) {
    super(), O_(this, e, z_, F_, M_, {
      likeable: 1,
      clickable: 2,
      value: 0,
      action_label: 3
    });
  }
  get likeable() {
    return this.$$.ctx[1];
  }
  set likeable(e) {
    this.$$set({
      likeable: e
    }), el();
  }
  get clickable() {
    return this.$$.ctx[2];
  }
  set clickable(e) {
    this.$$set({
      clickable: e
    }), el();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({
      value: e
    }), el();
  }
  get action_label() {
    return this.$$.ctx[3];
  }
  set action_label(e) {
    this.$$set({
      action_label: e
    }), el();
  }
}
const fi = [{
  key: "xs",
  width: 0
}, {
  key: "sm",
  width: 576
}, {
  key: "md",
  width: 768
}, {
  key: "lg",
  width: 992
}, {
  key: "xl",
  width: 1200
}, {
  key: "xxl",
  width: 1600
}];
async function q_(l) {
  if ("clipboard" in navigator)
    await navigator.clipboard.writeText(l);
  else {
    const e = document.createElement("textarea");
    e.value = l, e.style.position = "absolute", e.style.left = "-999999px", document.body.prepend(e), e.select();
    try {
      document.execCommand("copy");
    } catch (t) {
      return Promise.reject(t);
    } finally {
      e.remove();
    }
  }
}
async function j_(l) {
  return l ? `<div style="display: flex; flex-wrap: wrap; gap: 16px">${(await Promise.all(l.map((t) => !t.image || !t.image.url ? "" : t.image.url))).map((t) => `<img src="${t}" style="height: 400px" />`).join("")}</div>` : "";
}
function H_(l) {
  let e = 0;
  for (let t = 0; t < l.length; t++) e = l[e] <= l[t] ? e : t;
  return e;
}
function V_(l, {
  getWidth: e,
  setWidth: t,
  getHeight: n,
  setHeight: i,
  getPadding: o,
  setX: s,
  setY: f,
  getChildren: a
}, {
  cols: r,
  gap: c
}) {
  const [u, _, m, p] = o(l), y = a(l), C = y.length, [E, b] = Array.isArray(c) ? c : [c, c];
  if (C) {
    const v = (e(l) - E * (r - 1) - (p + _)) / r;
    y.forEach((w) => {
      t(w, v);
    });
    const g = y.map((w) => n(w)), S = Array(r).fill(u);
    for (let w = 0; w < C; w++) {
      const L = y[w], A = H_(S);
      f(L, S[A]), s(L, p + (v + E) * A), S[A] += g[w] + b;
    }
    i(l, Math.max(...S) - b + m);
  } else
    i(l, u + m);
}
const yr = (l) => l.nodeType == 1, Ai = Symbol(), Si = Symbol();
function W_(l, e) {
  let t, n, i = !1;
  function o() {
    i || (i = !0, requestAnimationFrame(() => {
      e(), l[Si] = l.offsetWidth, l[Ai] = l.offsetHeight, i = !1;
    }));
  }
  function s() {
    l && (t = new ResizeObserver((a) => {
      a.some((r) => {
        const c = r.target;
        return c[Si] !== c.offsetWidth || c[Ai] !== c.offsetHeight;
      }) && o();
    }), t.observe(l), Array.from(l.children).forEach((a) => {
      t.observe(a);
    }), n = new MutationObserver((a) => {
      a.forEach((r) => {
        r.addedNodes.forEach((c) => yr(c) && t.observe(c)), r.removedNodes.forEach((c) => yr(c) && t.unobserve(c));
      }), o();
    }), n.observe(l, {
      childList: !0,
      attributes: !1
    }), o());
  }
  function f() {
    t == null || t.disconnect(), n == null || n.disconnect();
  }
  return {
    layout: o,
    mount: s,
    unmount: f
  };
}
const G_ = (l, e) => W_(l, () => {
  V_(l, {
    getWidth: (t) => t.offsetWidth,
    setWidth: (t, n) => t.style.width = n + "px",
    getHeight: (t) => (t[Si] = t.offsetWidth, t[Ai] = t.offsetHeight),
    setHeight: (t, n) => t.style.height = n + "px",
    getPadding: (t) => {
      const n = getComputedStyle(t);
      return [parseInt(n.paddingTop), parseInt(n.paddingRight), parseInt(n.paddingBottom), parseInt(n.paddingLeft)];
    },
    setX: (t, n) => t.style.left = n + "px",
    setY: (t, n) => t.style.top = n + "px",
    getChildren: (t) => Array.from(t.children)
  }, e);
});
class Y_ {
  constructor(e, t = {
    cols: 2,
    gap: 4
  }) {
    Ce(this, "_layout");
    this._layout = G_(e, t), this._layout.mount();
  }
  unmount() {
    this._layout.unmount();
  }
  render() {
    this._layout.layout();
  }
}
const {
  SvelteComponent: X_,
  add_iframe_resize_listener: Z_,
  add_render_callback: Aa,
  append_hydration: le,
  assign: K_,
  attr: M,
  binding_callbacks: ci,
  bubble: J_,
  check_outros: It,
  children: ye,
  claim_component: ht,
  claim_element: ce,
  claim_space: rt,
  claim_text: Sa,
  create_component: gt,
  destroy_component: bt,
  destroy_each: Ca,
  detach: Y,
  element: ue,
  empty: Tr,
  ensure_array_like: dl,
  get_spread_object: Q_,
  get_spread_update: x_,
  globals: $_,
  group_outros: Rt,
  init: ed,
  insert_hydration: Xe,
  listen: ml,
  mount_component: pt,
  noop: td,
  run_all: nd,
  safe_not_equal: ld,
  set_data: La,
  set_style: Tt,
  space: at,
  src_url_equal: hl,
  text: Ia,
  toggle_class: De,
  transition_in: B,
  transition_out: Z
} = window.__gradio__svelte__internal, {
  window: Ci
} = $_, {
  createEventDispatcher: id,
  onDestroy: od,
  tick: rd
} = window.__gradio__svelte__internal;
function Ar(l, e, t) {
  const n = l.slice();
  return n[57] = e[t], n[59] = t, n;
}
function Sr(l, e, t) {
  const n = l.slice();
  return n[57] = e[t], n[60] = e, n[59] = t, n;
}
function Cr(l) {
  let e, t;
  return e = new ws({
    props: {
      show_label: (
        /*show_label*/
        l[2]
      ),
      Icon: Br,
      label: (
        /*label*/
        l[4] || "Gallery"
      )
    }
  }), {
    c() {
      gt(e.$$.fragment);
    },
    l(n) {
      ht(e.$$.fragment, n);
    },
    m(n, i) {
      pt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*show_label*/
      4 && (o.show_label = /*show_label*/
      n[2]), i[0] & /*label*/
      16 && (o.label = /*label*/
      n[4] || "Gallery"), e.$set(o);
    },
    i(n) {
      t || (B(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Z(e.$$.fragment, n), t = !1;
    },
    d(n) {
      bt(e, n);
    }
  };
}
function ad(l) {
  let e, t, n, i, o, s, f, a, r, c, u, _ = (
    /*selected_image*/
    l[23] && /*allow_preview*/
    l[9] && Lr(l)
  ), m = (
    /*show_share_button*/
    l[10] && Nr(l)
  ), p = dl(
    /*resolved_value*/
    l[18]
  ), y = [];
  for (let g = 0; g < p.length; g += 1)
    y[g] = Or(Ar(l, p, g));
  const C = (g) => Z(y[g], 1, 1, () => {
    y[g] = null;
  }), E = [cd, fd], b = [];
  function v(g, S) {
    return (
      /*pending*/
      g[5] ? 0 : 1
    );
  }
  return a = v(l), r = b[a] = E[a](l), {
    c() {
      _ && _.c(), e = at(), t = ue("div"), n = ue("div"), m && m.c(), i = at(), o = ue("div");
      for (let g = 0; g < y.length; g += 1)
        y[g].c();
      s = at(), f = ue("p"), r.c(), this.h();
    },
    l(g) {
      _ && _.l(g), e = rt(g), t = ce(g, "DIV", {
        class: !0,
        style: !0
      });
      var S = ye(t);
      n = ce(S, "DIV", {
        class: !0,
        style: !0
      });
      var w = ye(n);
      m && m.l(w), i = rt(w), o = ce(w, "DIV", {
        class: !0
      });
      var L = ye(o);
      for (let q = 0; q < y.length; q += 1)
        y[q].l(L);
      L.forEach(Y), w.forEach(Y), s = rt(S), f = ce(S, "P", {
        class: !0
      });
      var A = ye(f);
      r.l(A), A.forEach(Y), S.forEach(Y), this.h();
    },
    h() {
      M(o, "class", "waterfall svelte-yk2d08"), M(n, "class", "grid-container svelte-yk2d08"), Tt(
        n,
        "--object-fit",
        /*object_fit*/
        l[1]
      ), Tt(
        n,
        "min-height",
        /*height*/
        l[8] + "px"
      ), De(
        n,
        "pt-6",
        /*show_label*/
        l[2]
      ), M(f, "class", "loading-line svelte-yk2d08"), De(f, "visible", !/*selected_image*/
      (l[23] && /*allow_preview*/
      l[9]) && /*has_more*/
      l[3]), M(t, "class", "grid-wrap svelte-yk2d08"), Tt(
        t,
        "height",
        /*height*/
        l[8] + "px"
      ), Aa(() => (
        /*div2_elementresize_handler*/
        l[51].call(t)
      )), De(t, "fixed-height", !/*height*/
      l[8] || /*height*/
      l[8] === "auto");
    },
    m(g, S) {
      _ && _.m(g, S), Xe(g, e, S), Xe(g, t, S), le(t, n), m && m.m(n, null), le(n, i), le(n, o);
      for (let w = 0; w < y.length; w += 1)
        y[w] && y[w].m(o, null);
      l[49](o), le(t, s), le(t, f), b[a].m(f, null), c = Z_(
        t,
        /*div2_elementresize_handler*/
        l[51].bind(t)
      ), u = !0;
    },
    p(g, S) {
      if (/*selected_image*/
      g[23] && /*allow_preview*/
      g[9] ? _ ? (_.p(g, S), S[0] & /*selected_image, allow_preview*/
      8389120 && B(_, 1)) : (_ = Lr(g), _.c(), B(_, 1), _.m(e.parentNode, e)) : _ && (Rt(), Z(_, 1, 1, () => {
        _ = null;
      }), It()), /*show_share_button*/
      g[10] ? m ? (m.p(g, S), S[0] & /*show_share_button*/
      1024 && B(m, 1)) : (m = Nr(g), m.c(), B(m, 1), m.m(n, i)) : m && (Rt(), Z(m, 1, 1, () => {
        m = null;
      }), It()), S[0] & /*resolved_value, selected_index, likeable, clickable, action_label, dispatch*/
      17045569) {
        p = dl(
          /*resolved_value*/
          g[18]
        );
        let L;
        for (L = 0; L < p.length; L += 1) {
          const A = Ar(g, p, L);
          y[L] ? (y[L].p(A, S), B(y[L], 1)) : (y[L] = Or(A), y[L].c(), B(y[L], 1), y[L].m(o, null));
        }
        for (Rt(), L = p.length; L < y.length; L += 1)
          C(L);
        It();
      }
      (!u || S[0] & /*object_fit*/
      2) && Tt(
        n,
        "--object-fit",
        /*object_fit*/
        g[1]
      ), (!u || S[0] & /*height*/
      256) && Tt(
        n,
        "min-height",
        /*height*/
        g[8] + "px"
      ), (!u || S[0] & /*show_label*/
      4) && De(
        n,
        "pt-6",
        /*show_label*/
        g[2]
      );
      let w = a;
      a = v(g), a === w ? b[a].p(g, S) : (Rt(), Z(b[w], 1, 1, () => {
        b[w] = null;
      }), It(), r = b[a], r ? r.p(g, S) : (r = b[a] = E[a](g), r.c()), B(r, 1), r.m(f, null)), (!u || S[0] & /*selected_image, allow_preview, has_more*/
      8389128) && De(f, "visible", !/*selected_image*/
      (g[23] && /*allow_preview*/
      g[9]) && /*has_more*/
      g[3]), (!u || S[0] & /*height*/
      256) && Tt(
        t,
        "height",
        /*height*/
        g[8] + "px"
      ), (!u || S[0] & /*height*/
      256) && De(t, "fixed-height", !/*height*/
      g[8] || /*height*/
      g[8] === "auto");
    },
    i(g) {
      if (!u) {
        B(_), B(m);
        for (let S = 0; S < p.length; S += 1)
          B(y[S]);
        B(r), u = !0;
      }
    },
    o(g) {
      Z(_), Z(m), y = y.filter(Boolean);
      for (let S = 0; S < y.length; S += 1)
        Z(y[S]);
      Z(r), u = !1;
    },
    d(g) {
      g && (Y(e), Y(t)), _ && _.d(g), m && m.d(), Ca(y, g), l[49](null), b[a].d(), c();
    }
  };
}
function sd(l) {
  let e, t;
  return e = new xs({
    props: {
      unpadded_box: !0,
      size: "large",
      $$slots: {
        default: [_d]
      },
      $$scope: {
        ctx: l
      }
    }
  }), {
    c() {
      gt(e.$$.fragment);
    },
    l(n) {
      ht(e.$$.fragment, n);
    },
    m(n, i) {
      pt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[1] & /*$$scope*/
      1073741824 && (o.$$scope = {
        dirty: i,
        ctx: n
      }), e.$set(o);
    },
    i(n) {
      t || (B(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Z(e.$$.fragment, n), t = !1;
    },
    d(n) {
      bt(e, n);
    }
  };
}
function Lr(l) {
  var S;
  let e, t, n, i, o, s, f, a, r, c, u, _, m, p, y, C, E = (
    /*show_download_button*/
    l[13] && Ir(l)
  );
  i = new p_({
    props: {
      i18n: (
        /*i18n*/
        l[14]
      ),
      absolute: !1
    }
  }), i.$on(
    "clear",
    /*clear_handler*/
    l[39]
  );
  let b = (
    /*selected_image*/
    ((S = l[23]) == null ? void 0 : S.caption) && Rr(l)
  ), v = dl(
    /*resolved_value*/
    l[18]
  ), g = [];
  for (let w = 0; w < v.length; w += 1)
    g[w] = Dr(Sr(l, v, w));
  return {
    c() {
      e = ue("button"), t = ue("div"), E && E.c(), n = at(), gt(i.$$.fragment), o = at(), s = ue("button"), f = ue("img"), u = at(), b && b.c(), _ = at(), m = ue("div");
      for (let w = 0; w < g.length; w += 1)
        g[w].c();
      this.h();
    },
    l(w) {
      e = ce(w, "BUTTON", {
        class: !0
      });
      var L = ye(e);
      t = ce(L, "DIV", {
        class: !0
      });
      var A = ye(t);
      E && E.l(A), n = rt(A), ht(i.$$.fragment, A), A.forEach(Y), o = rt(L), s = ce(L, "BUTTON", {
        class: !0,
        style: !0,
        "aria-label": !0
      });
      var q = ye(s);
      f = ce(q, "IMG", {
        "data-testid": !0,
        src: !0,
        alt: !0,
        title: !0,
        loading: !0,
        class: !0
      }), q.forEach(Y), u = rt(L), b && b.l(L), _ = rt(L), m = ce(L, "DIV", {
        class: !0,
        "data-testid": !0
      });
      var F = ye(m);
      for (let P = 0; P < g.length; P += 1)
        g[P].l(F);
      F.forEach(Y), L.forEach(Y), this.h();
    },
    h() {
      M(t, "class", "icon-buttons svelte-yk2d08"), M(f, "data-testid", "detailed-image"), hl(f.src, a = /*selected_image*/
      l[23].image.url) || M(f, "src", a), M(f, "alt", r = /*selected_image*/
      l[23].caption || ""), M(f, "title", c = /*selected_image*/
      l[23].caption || null), M(f, "loading", "lazy"), M(f, "class", "svelte-yk2d08"), De(f, "with-caption", !!/*selected_image*/
      l[23].caption), M(s, "class", "image-button svelte-yk2d08"), Tt(s, "height", "calc(100% - " + /*selected_image*/
      (l[23].caption ? "80px" : "60px") + ")"), M(s, "aria-label", "detailed view of selected image"), M(m, "class", "thumbnails scroll-hide svelte-yk2d08"), M(m, "data-testid", "container_el"), M(e, "class", "preview svelte-yk2d08");
    },
    m(w, L) {
      Xe(w, e, L), le(e, t), E && E.m(t, null), le(t, n), pt(i, t, null), le(e, o), le(e, s), le(s, f), le(e, u), b && b.m(e, null), le(e, _), le(e, m);
      for (let A = 0; A < g.length; A += 1)
        g[A] && g[A].m(m, null);
      l[43](m), p = !0, y || (C = [ml(
        s,
        "click",
        /*click_handler_1*/
        l[40]
      ), ml(
        e,
        "keydown",
        /*on_keydown*/
        l[26]
      )], y = !0);
    },
    p(w, L) {
      var q;
      /*show_download_button*/
      w[13] ? E ? (E.p(w, L), L[0] & /*show_download_button*/
      8192 && B(E, 1)) : (E = Ir(w), E.c(), B(E, 1), E.m(t, n)) : E && (Rt(), Z(E, 1, 1, () => {
        E = null;
      }), It());
      const A = {};
      if (L[0] & /*i18n*/
      16384 && (A.i18n = /*i18n*/
      w[14]), i.$set(A), (!p || L[0] & /*selected_image*/
      8388608 && !hl(f.src, a = /*selected_image*/
      w[23].image.url)) && M(f, "src", a), (!p || L[0] & /*selected_image*/
      8388608 && r !== (r = /*selected_image*/
      w[23].caption || "")) && M(f, "alt", r), (!p || L[0] & /*selected_image*/
      8388608 && c !== (c = /*selected_image*/
      w[23].caption || null)) && M(f, "title", c), (!p || L[0] & /*selected_image*/
      8388608) && De(f, "with-caption", !!/*selected_image*/
      w[23].caption), (!p || L[0] & /*selected_image*/
      8388608) && Tt(s, "height", "calc(100% - " + /*selected_image*/
      (w[23].caption ? "80px" : "60px") + ")"), /*selected_image*/
      (q = w[23]) != null && q.caption ? b ? b.p(w, L) : (b = Rr(w), b.c(), b.m(e, _)) : b && (b.d(1), b = null), L[0] & /*resolved_value, el, selected_index*/
      2359297) {
        v = dl(
          /*resolved_value*/
          w[18]
        );
        let F;
        for (F = 0; F < v.length; F += 1) {
          const P = Sr(w, v, F);
          g[F] ? g[F].p(P, L) : (g[F] = Dr(P), g[F].c(), g[F].m(m, null));
        }
        for (; F < g.length; F += 1)
          g[F].d(1);
        g.length = v.length;
      }
    },
    i(w) {
      p || (B(E), B(i.$$.fragment, w), p = !0);
    },
    o(w) {
      Z(E), Z(i.$$.fragment, w), p = !1;
    },
    d(w) {
      w && Y(e), E && E.d(), bt(i), b && b.d(), Ca(g, w), l[43](null), y = !1, nd(C);
    }
  };
}
function Ir(l) {
  let e, t, n;
  return t = new St({
    props: {
      show_label: !0,
      label: (
        /*i18n*/
        l[14]("common.download")
      ),
      Icon: zr
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[38]
  ), {
    c() {
      e = ue("div"), gt(t.$$.fragment), this.h();
    },
    l(i) {
      e = ce(i, "DIV", {
        class: !0
      });
      var o = ye(e);
      ht(t.$$.fragment, o), o.forEach(Y), this.h();
    },
    h() {
      M(e, "class", "download-button-container svelte-yk2d08");
    },
    m(i, o) {
      Xe(i, e, o), pt(t, e, null), n = !0;
    },
    p(i, o) {
      const s = {};
      o[0] & /*i18n*/
      16384 && (s.label = /*i18n*/
      i[14]("common.download")), t.$set(s);
    },
    i(i) {
      n || (B(t.$$.fragment, i), n = !0);
    },
    o(i) {
      Z(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && Y(e), bt(t);
    }
  };
}
function Rr(l) {
  let e, t = (
    /*selected_image*/
    l[23].caption + ""
  ), n;
  return {
    c() {
      e = ue("caption"), n = Ia(t), this.h();
    },
    l(i) {
      e = ce(i, "CAPTION", {
        class: !0
      });
      var o = ye(e);
      n = Sa(o, t), o.forEach(Y), this.h();
    },
    h() {
      M(e, "class", "caption svelte-yk2d08");
    },
    m(i, o) {
      Xe(i, e, o), le(e, n);
    },
    p(i, o) {
      o[0] & /*selected_image*/
      8388608 && t !== (t = /*selected_image*/
      i[23].caption + "") && La(n, t);
    },
    d(i) {
      i && Y(e);
    }
  };
}
function Dr(l) {
  let e, t, n, i, o, s, f = (
    /*i*/
    l[59]
  ), a, r;
  const c = () => (
    /*button_binding*/
    l[41](e, f)
  ), u = () => (
    /*button_binding*/
    l[41](null, f)
  );
  function _() {
    return (
      /*click_handler_2*/
      l[42](
        /*i*/
        l[59]
      )
    );
  }
  return {
    c() {
      e = ue("button"), t = ue("img"), o = at(), this.h();
    },
    l(m) {
      e = ce(m, "BUTTON", {
        class: !0,
        "aria-label": !0
      });
      var p = ye(e);
      t = ce(p, "IMG", {
        src: !0,
        title: !0,
        "data-testid": !0,
        alt: !0,
        loading: !0,
        class: !0
      }), o = rt(p), p.forEach(Y), this.h();
    },
    h() {
      hl(t.src, n = /*entry*/
      l[57].image.url) || M(t, "src", n), M(t, "title", i = /*entry*/
      l[57].caption || null), M(t, "data-testid", "thumbnail " + /*i*/
      (l[59] + 1)), M(t, "alt", ""), M(t, "loading", "lazy"), M(t, "class", "svelte-yk2d08"), M(e, "class", "thumbnail-item thumbnail-small svelte-yk2d08"), M(e, "aria-label", s = "Thumbnail " + /*i*/
      (l[59] + 1) + " of " + /*resolved_value*/
      l[18].length), De(
        e,
        "selected",
        /*selected_index*/
        l[0] === /*i*/
        l[59]
      );
    },
    m(m, p) {
      Xe(m, e, p), le(e, t), le(e, o), c(), a || (r = ml(e, "click", _), a = !0);
    },
    p(m, p) {
      l = m, p[0] & /*resolved_value*/
      262144 && !hl(t.src, n = /*entry*/
      l[57].image.url) && M(t, "src", n), p[0] & /*resolved_value*/
      262144 && i !== (i = /*entry*/
      l[57].caption || null) && M(t, "title", i), p[0] & /*resolved_value*/
      262144 && s !== (s = "Thumbnail " + /*i*/
      (l[59] + 1) + " of " + /*resolved_value*/
      l[18].length) && M(e, "aria-label", s), f !== /*i*/
      l[59] && (u(), f = /*i*/
      l[59], c()), p[0] & /*selected_index*/
      1 && De(
        e,
        "selected",
        /*selected_index*/
        l[0] === /*i*/
        l[59]
      );
    },
    d(m) {
      m && Y(e), u(), a = !1, r();
    }
  };
}
function Nr(l) {
  let e, t, n;
  return t = new ic({
    props: {
      i18n: (
        /*i18n*/
        l[14]
      ),
      value: (
        /*resolved_value*/
        l[18]
      ),
      formatter: j_
    }
  }), t.$on(
    "share",
    /*share_handler*/
    l[44]
  ), t.$on(
    "error",
    /*error_handler*/
    l[45]
  ), {
    c() {
      e = ue("div"), gt(t.$$.fragment), this.h();
    },
    l(i) {
      e = ce(i, "DIV", {
        class: !0
      });
      var o = ye(e);
      ht(t.$$.fragment, o), o.forEach(Y), this.h();
    },
    h() {
      M(e, "class", "icon-button svelte-yk2d08");
    },
    m(i, o) {
      Xe(i, e, o), pt(t, e, null), n = !0;
    },
    p(i, o) {
      const s = {};
      o[0] & /*i18n*/
      16384 && (s.i18n = /*i18n*/
      i[14]), o[0] & /*resolved_value*/
      262144 && (s.value = /*resolved_value*/
      i[18]), t.$set(s);
    },
    i(i) {
      n || (B(t.$$.fragment, i), n = !0);
    },
    o(i) {
      Z(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && Y(e), bt(t);
    }
  };
}
function Or(l) {
  let e, t, n, i, o;
  function s() {
    return (
      /*click_handler_3*/
      l[46](
        /*i*/
        l[59]
      )
    );
  }
  function f() {
    return (
      /*label_click_handler*/
      l[47](
        /*i*/
        l[59],
        /*entry*/
        l[57]
      )
    );
  }
  function a(...r) {
    return (
      /*like_handler*/
      l[48](
        /*i*/
        l[59],
        /*entry*/
        l[57],
        ...r
      )
    );
  }
  return t = new B_({
    props: {
      likeable: (
        /*likeable*/
        l[11]
      ),
      clickable: (
        /*clickable*/
        l[12]
      ),
      value: (
        /*entry*/
        l[57]
      ),
      action_label: (
        /*action_label*/
        l[6]
      )
    }
  }), t.$on("click", s), t.$on("label_click", f), t.$on("like", a), {
    c() {
      e = ue("div"), gt(t.$$.fragment), n = at(), this.h();
    },
    l(r) {
      e = ce(r, "DIV", {
        class: !0,
        "aria-label": !0
      });
      var c = ye(e);
      ht(t.$$.fragment, c), n = rt(c), c.forEach(Y), this.h();
    },
    h() {
      M(e, "class", "thumbnail-item thumbnail-lg svelte-yk2d08"), M(e, "aria-label", i = "Thumbnail " + /*i*/
      (l[59] + 1) + " of " + /*resolved_value*/
      l[18].length), De(
        e,
        "selected",
        /*selected_index*/
        l[0] === /*i*/
        l[59]
      );
    },
    m(r, c) {
      Xe(r, e, c), pt(t, e, null), le(e, n), o = !0;
    },
    p(r, c) {
      l = r;
      const u = {};
      c[0] & /*likeable*/
      2048 && (u.likeable = /*likeable*/
      l[11]), c[0] & /*clickable*/
      4096 && (u.clickable = /*clickable*/
      l[12]), c[0] & /*resolved_value*/
      262144 && (u.value = /*entry*/
      l[57]), c[0] & /*action_label*/
      64 && (u.action_label = /*action_label*/
      l[6]), t.$set(u), (!o || c[0] & /*resolved_value*/
      262144 && i !== (i = "Thumbnail " + /*i*/
      (l[59] + 1) + " of " + /*resolved_value*/
      l[18].length)) && M(e, "aria-label", i), (!o || c[0] & /*selected_index*/
      1) && De(
        e,
        "selected",
        /*selected_index*/
        l[0] === /*i*/
        l[59]
      );
    },
    i(r) {
      o || (B(t.$$.fragment, r), o = !0);
    },
    o(r) {
      Z(t.$$.fragment, r), o = !1;
    },
    d(r) {
      r && Y(e), bt(t);
    }
  };
}
function fd(l) {
  let e, t;
  const n = [
    /*load_more_button_props*/
    l[15]
  ];
  let i = {
    $$slots: {
      default: [ud]
    },
    $$scope: {
      ctx: l
    }
  };
  for (let o = 0; o < n.length; o += 1)
    i = K_(i, n[o]);
  return e = new qu({
    props: i
  }), e.$on(
    "click",
    /*click_handler_4*/
    l[50]
  ), {
    c() {
      gt(e.$$.fragment);
    },
    l(o) {
      ht(e.$$.fragment, o);
    },
    m(o, s) {
      pt(e, o, s), t = !0;
    },
    p(o, s) {
      const f = s[0] & /*load_more_button_props*/
      32768 ? x_(n, [Q_(
        /*load_more_button_props*/
        o[15]
      )]) : {};
      s[0] & /*i18n, load_more_button_props*/
      49152 | s[1] & /*$$scope*/
      1073741824 && (f.$$scope = {
        dirty: s,
        ctx: o
      }), e.$set(f);
    },
    i(o) {
      t || (B(e.$$.fragment, o), t = !0);
    },
    o(o) {
      Z(e.$$.fragment, o), t = !1;
    },
    d(o) {
      bt(e, o);
    }
  };
}
function cd(l) {
  let e, t;
  return e = new Vr({
    props: {
      margin: !1
    }
  }), {
    c() {
      gt(e.$$.fragment);
    },
    l(n) {
      ht(e.$$.fragment, n);
    },
    m(n, i) {
      pt(e, n, i), t = !0;
    },
    p: td,
    i(n) {
      t || (B(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Z(e.$$.fragment, n), t = !1;
    },
    d(n) {
      bt(e, n);
    }
  };
}
function ud(l) {
  let e = (
    /*i18n*/
    l[14](
      /*load_more_button_props*/
      l[15].value || /*load_more_button_props*/
      l[15].label || "Load More"
    ) + ""
  ), t;
  return {
    c() {
      t = Ia(e);
    },
    l(n) {
      t = Sa(n, e);
    },
    m(n, i) {
      Xe(n, t, i);
    },
    p(n, i) {
      i[0] & /*i18n, load_more_button_props*/
      49152 && e !== (e = /*i18n*/
      n[14](
        /*load_more_button_props*/
        n[15].value || /*load_more_button_props*/
        n[15].label || "Load More"
      ) + "") && La(t, e);
    },
    d(n) {
      n && Y(t);
    }
  };
}
function _d(l) {
  let e, t;
  return e = new Br({}), {
    c() {
      gt(e.$$.fragment);
    },
    l(n) {
      ht(e.$$.fragment, n);
    },
    m(n, i) {
      pt(e, n, i), t = !0;
    },
    i(n) {
      t || (B(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Z(e.$$.fragment, n), t = !1;
    },
    d(n) {
      bt(e, n);
    }
  };
}
function dd(l) {
  let e, t, n, i, o, s, f;
  Aa(
    /*onwindowresize*/
    l[37]
  );
  let a = (
    /*show_label*/
    l[2] && Cr(l)
  );
  const r = [sd, ad], c = [];
  function u(_, m) {
    return !/*value*/
    _[7] || !/*resolved_value*/
    _[18] || /*resolved_value*/
    _[18].length === 0 ? 0 : 1;
  }
  return t = u(l), n = c[t] = r[t](l), {
    c() {
      a && a.c(), e = at(), n.c(), i = Tr();
    },
    l(_) {
      a && a.l(_), e = rt(_), n.l(_), i = Tr();
    },
    m(_, m) {
      a && a.m(_, m), Xe(_, e, m), c[t].m(_, m), Xe(_, i, m), o = !0, s || (f = ml(
        Ci,
        "resize",
        /*onwindowresize*/
        l[37]
      ), s = !0);
    },
    p(_, m) {
      /*show_label*/
      _[2] ? a ? (a.p(_, m), m[0] & /*show_label*/
      4 && B(a, 1)) : (a = Cr(_), a.c(), B(a, 1), a.m(e.parentNode, e)) : a && (Rt(), Z(a, 1, 1, () => {
        a = null;
      }), It());
      let p = t;
      t = u(_), t === p ? c[t].p(_, m) : (Rt(), Z(c[p], 1, 1, () => {
        c[p] = null;
      }), It(), n = c[t], n ? n.p(_, m) : (n = c[t] = r[t](_), n.c()), B(n, 1), n.m(i.parentNode, i));
    },
    i(_) {
      o || (B(a), B(n), o = !0);
    },
    o(_) {
      Z(a), Z(n), o = !1;
    },
    d(_) {
      _ && (Y(e), Y(i)), a && a.d(_), c[t].d(_), s = !1, f();
    }
  };
}
async function md(l, e) {
  let t;
  try {
    t = await fetch(l);
  } catch (s) {
    if (s instanceof TypeError) {
      window.open(l, "_blank", "noreferrer");
      return;
    }
    throw s;
  }
  const n = await t.blob(), i = URL.createObjectURL(n), o = document.createElement("a");
  o.href = i, o.download = e, o.click(), URL.revokeObjectURL(i);
}
function hd(l, e, t) {
  let n, i, o, {
    object_fit: s = "cover"
  } = e, {
    show_label: f = !0
  } = e, {
    has_more: a = !1
  } = e, {
    label: r
  } = e, {
    pending: c
  } = e, {
    action_label: u
  } = e, {
    value: _ = null
  } = e, {
    columns: m = [2]
  } = e, {
    height: p = "auto"
  } = e, {
    preview: y
  } = e, {
    root: C
  } = e, {
    proxy_url: E
  } = e, {
    allow_preview: b = !0
  } = e, {
    show_share_button: v = !1
  } = e, {
    likeable: g
  } = e, {
    clickable: S
  } = e, {
    show_download_button: w = !1
  } = e, {
    i18n: L
  } = e, {
    selected_index: A = null
  } = e, {
    gap: q = 8
  } = e, {
    load_more_button_props: F = {}
  } = e, P, j = [], de, x = 0, Ae = 0, ee = 0;
  const ke = id();
  let Se = !0, re = null, G = null, z = _;
  A == null && y && (_ != null && _.length) && (A = 0);
  let Ze = A;
  function W(k) {
    const H = k.target, te = k.clientX, zt = H.offsetWidth / 2;
    te < zt ? t(0, A = n) : t(0, A = i);
  }
  function wt(k) {
    switch (k.code) {
      case "Escape":
        k.preventDefault(), t(0, A = null);
        break;
      case "ArrowLeft":
        k.preventDefault(), t(0, A = n);
        break;
      case "ArrowRight":
        k.preventDefault(), t(0, A = i);
        break;
    }
  }
  const h = [];
  let me;
  async function $t(k) {
    var an;
    if (typeof k != "number" || (await rd(), h[k] === void 0)) return;
    (an = h[k]) == null || an.focus();
    const {
      left: H,
      width: te
    } = me.getBoundingClientRect(), {
      left: rn,
      width: zt
    } = h[k].getBoundingClientRect(), Bt = rn - H + zt / 2 - te / 2 + me.scrollLeft;
    me && typeof me.scrollTo == "function" && me.scrollTo({
      left: Bt < 0 ? 0 : Bt,
      behavior: "smooth"
    });
  }
  function In() {
    re == null || re.unmount(), re = new Y_(P, {
      cols: de,
      gap: q
    });
  }
  od(() => {
    re == null || re.unmount();
  });
  function en() {
    t(20, Ae = Ci.innerHeight), t(17, ee = Ci.innerWidth);
  }
  const Rn = () => {
    const k = o == null ? void 0 : o.image;
    if (!k)
      return;
    const {
      url: H,
      orig_name: te
    } = k;
    H && md(H, te ?? "image");
  }, Dn = () => t(0, A = null), kt = (k) => W(k);
  function tn(k, H) {
    ci[k ? "unshift" : "push"](() => {
      h[H] = k, t(21, h);
    });
  }
  const st = (k) => t(0, A = k);
  function nn(k) {
    ci[k ? "unshift" : "push"](() => {
      me = k, t(22, me);
    });
  }
  const ln = (k) => {
    q_(k.detail.description);
  };
  function vt(k) {
    J_.call(this, l, k);
  }
  const Ut = (k) => t(0, A = k), Ft = (k, H) => {
    ke("click", {
      index: k,
      value: H
    });
  }, Nn = (k, H, te) => {
    ke("like", {
      index: k,
      value: H,
      liked: te.detail
    });
  };
  function On(k) {
    ci[k ? "unshift" : "push"](() => {
      P = k, t(16, P);
    });
  }
  const kl = () => {
    ke("load_more");
  };
  function on() {
    x = this.clientHeight, t(19, x);
  }
  return l.$$set = (k) => {
    "object_fit" in k && t(1, s = k.object_fit), "show_label" in k && t(2, f = k.show_label), "has_more" in k && t(3, a = k.has_more), "label" in k && t(4, r = k.label), "pending" in k && t(5, c = k.pending), "action_label" in k && t(6, u = k.action_label), "value" in k && t(7, _ = k.value), "columns" in k && t(27, m = k.columns), "height" in k && t(8, p = k.height), "preview" in k && t(28, y = k.preview), "root" in k && t(29, C = k.root), "proxy_url" in k && t(30, E = k.proxy_url), "allow_preview" in k && t(9, b = k.allow_preview), "show_share_button" in k && t(10, v = k.show_share_button), "likeable" in k && t(11, g = k.likeable), "clickable" in k && t(12, S = k.clickable), "show_download_button" in k && t(13, w = k.show_download_button), "i18n" in k && t(14, L = k.i18n), "selected_index" in k && t(0, A = k.selected_index), "gap" in k && t(31, q = k.gap), "load_more_button_props" in k && t(15, F = k.load_more_button_props);
  }, l.$$.update = () => {
    if (l.$$.dirty[0] & /*columns*/
    134217728)
      if (typeof m == "object" && m !== null)
        if (Array.isArray(m)) {
          const k = m.length;
          t(32, j = fi.map((H, te) => [H.width, m[te] ?? m[k - 1]]));
        } else {
          let k = 0;
          t(32, j = fi.map((H) => (k = m[H.key] ?? k, [H.width, k])));
        }
      else
        t(32, j = fi.map((k) => [k.width, m]));
    if (l.$$.dirty[0] & /*window_width*/
    131072 | l.$$.dirty[1] & /*breakpointColumns*/
    2) {
      for (const [k, H] of [...j].reverse())
        if (ee >= k) {
          t(33, de = H);
          break;
        }
    }
    l.$$.dirty[0] & /*value*/
    128 | l.$$.dirty[1] & /*was_reset*/
    8 && t(34, Se = _ == null || _.length === 0 ? !0 : Se), l.$$.dirty[0] & /*value, root, proxy_url*/
    1610612864 && t(18, G = _ == null ? null : _.map((k) => (k.image = ka(k.image, C, E), k))), l.$$.dirty[0] & /*value, preview, selected_index*/
    268435585 | l.$$.dirty[1] & /*prev_value, was_reset*/
    24 && (vn(z, _) || (Se ? (t(0, A = y && (_ != null && _.length) ? 0 : null), t(34, Se = !1), re = null) : t(0, A = A != null && _ != null && A < _.length ? A : null), ke("change"), t(35, z = _))), l.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 && (n = ((A ?? 0) + ((G == null ? void 0 : G.length) ?? 0) - 1) % ((G == null ? void 0 : G.length) ?? 0)), l.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 && (i = ((A ?? 0) + 1) % ((G == null ? void 0 : G.length) ?? 0)), l.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 | l.$$.dirty[1] & /*old_selected_index*/
    32 && A !== Ze && (t(36, Ze = A), A !== null && ke("select", {
      index: A,
      value: G == null ? void 0 : G[A]
    })), l.$$.dirty[0] & /*allow_preview, selected_index*/
    513 && b && $t(A), l.$$.dirty[0] & /*waterfall_grid_el*/
    65536 | l.$$.dirty[1] & /*cols*/
    4 && P && In(), l.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 && t(23, o = A != null && G != null ? G[A] : null);
  }, [A, s, f, a, r, c, u, _, p, b, v, g, S, w, L, F, P, ee, G, x, Ae, h, me, o, ke, W, wt, m, y, C, E, q, j, de, Se, z, Ze, en, Rn, Dn, kt, tn, st, nn, ln, vt, Ut, Ft, Nn, On, kl, on];
}
class gd extends X_ {
  constructor(e) {
    super(), ed(this, e, hd, dd, ld, {
      object_fit: 1,
      show_label: 2,
      has_more: 3,
      label: 4,
      pending: 5,
      action_label: 6,
      value: 7,
      columns: 27,
      height: 8,
      preview: 28,
      root: 29,
      proxy_url: 30,
      allow_preview: 9,
      show_share_button: 10,
      likeable: 11,
      clickable: 12,
      show_download_button: 13,
      i18n: 14,
      selected_index: 0,
      gap: 31,
      load_more_button_props: 15
    }, null, [-1, -1]);
  }
}
const {
  SvelteComponent: bd,
  add_flush_callback: pd,
  assign: wd,
  bind: kd,
  binding_callbacks: vd,
  check_outros: Ed,
  claim_component: Ni,
  claim_space: yd,
  create_component: Oi,
  destroy_component: Mi,
  detach: Td,
  get_spread_object: Ad,
  get_spread_update: Sd,
  group_outros: Cd,
  init: Ld,
  insert_hydration: Id,
  mount_component: Pi,
  safe_not_equal: Rd,
  space: Dd,
  transition_in: Kt,
  transition_out: yn
} = window.__gradio__svelte__internal, {
  createEventDispatcher: Nd
} = window.__gradio__svelte__internal;
function Mr(l) {
  let e, t;
  const n = [
    {
      autoscroll: (
        /*gradio*/
        l[25].autoscroll
      )
    },
    {
      i18n: (
        /*gradio*/
        l[25].i18n
      )
    },
    /*loading_status*/
    l[1],
    {
      show_progress: (
        /*loading_status*/
        l[1].show_progress === "hidden" ? "hidden" : (
          /*has_more*/
          l[3] ? "minimal" : (
            /*loading_status*/
            l[1].show_progress
          )
        )
      )
    }
  ];
  let i = {};
  for (let o = 0; o < n.length; o += 1)
    i = wd(i, n[o]);
  return e = new fu({
    props: i
  }), {
    c() {
      Oi(e.$$.fragment);
    },
    l(o) {
      Ni(e.$$.fragment, o);
    },
    m(o, s) {
      Pi(e, o, s), t = !0;
    },
    p(o, s) {
      const f = s[0] & /*gradio, loading_status, has_more*/
      33554442 ? Sd(n, [s[0] & /*gradio*/
      33554432 && {
        autoscroll: (
          /*gradio*/
          o[25].autoscroll
        )
      }, s[0] & /*gradio*/
      33554432 && {
        i18n: (
          /*gradio*/
          o[25].i18n
        )
      }, s[0] & /*loading_status*/
      2 && Ad(
        /*loading_status*/
        o[1]
      ), s[0] & /*loading_status, has_more*/
      10 && {
        show_progress: (
          /*loading_status*/
          o[1].show_progress === "hidden" ? "hidden" : (
            /*has_more*/
            o[3] ? "minimal" : (
              /*loading_status*/
              o[1].show_progress
            )
          )
        )
      }]) : {};
      e.$set(f);
    },
    i(o) {
      t || (Kt(e.$$.fragment, o), t = !0);
    },
    o(o) {
      yn(e.$$.fragment, o), t = !1;
    },
    d(o) {
      Mi(e, o);
    }
  };
}
function Od(l) {
  var a;
  let e, t, n, i, o = (
    /*loading_status*/
    l[1] && Mr(l)
  );
  function s(r) {
    l[29](r);
  }
  let f = {
    pending: (
      /*loading_status*/
      ((a = l[1]) == null ? void 0 : a.status) === "pending"
    ),
    likeable: (
      /*likeable*/
      l[10]
    ),
    clickable: (
      /*clickable*/
      l[11]
    ),
    label: (
      /*label*/
      l[4]
    ),
    action_label: (
      /*action_label*/
      l[5]
    ),
    value: (
      /*value*/
      l[9]
    ),
    root: (
      /*root*/
      l[23]
    ),
    proxy_url: (
      /*proxy_url*/
      l[24]
    ),
    show_label: (
      /*show_label*/
      l[2]
    ),
    object_fit: (
      /*object_fit*/
      l[21]
    ),
    load_more_button_props: (
      /*_load_more_button_props*/
      l[26]
    ),
    has_more: (
      /*has_more*/
      l[3]
    ),
    columns: (
      /*columns*/
      l[15]
    ),
    height: (
      /*height*/
      l[17]
    ),
    preview: (
      /*preview*/
      l[18]
    ),
    gap: (
      /*gap*/
      l[16]
    ),
    allow_preview: (
      /*allow_preview*/
      l[19]
    ),
    show_share_button: (
      /*show_share_button*/
      l[20]
    ),
    show_download_button: (
      /*show_download_button*/
      l[22]
    ),
    i18n: (
      /*gradio*/
      l[25].i18n
    )
  };
  return (
    /*selected_index*/
    l[0] !== void 0 && (f.selected_index = /*selected_index*/
    l[0]), t = new gd({
      props: f
    }), vd.push(() => kd(t, "selected_index", s)), t.$on(
      "click",
      /*click_handler*/
      l[30]
    ), t.$on(
      "change",
      /*change_handler*/
      l[31]
    ), t.$on(
      "like",
      /*like_handler*/
      l[32]
    ), t.$on(
      "select",
      /*select_handler*/
      l[33]
    ), t.$on(
      "share",
      /*share_handler*/
      l[34]
    ), t.$on(
      "error",
      /*error_handler*/
      l[35]
    ), t.$on(
      "load_more",
      /*load_more_handler*/
      l[36]
    ), {
      c() {
        o && o.c(), e = Dd(), Oi(t.$$.fragment);
      },
      l(r) {
        o && o.l(r), e = yd(r), Ni(t.$$.fragment, r);
      },
      m(r, c) {
        o && o.m(r, c), Id(r, e, c), Pi(t, r, c), i = !0;
      },
      p(r, c) {
        var _;
        /*loading_status*/
        r[1] ? o ? (o.p(r, c), c[0] & /*loading_status*/
        2 && Kt(o, 1)) : (o = Mr(r), o.c(), Kt(o, 1), o.m(e.parentNode, e)) : o && (Cd(), yn(o, 1, 1, () => {
          o = null;
        }), Ed());
        const u = {};
        c[0] & /*loading_status*/
        2 && (u.pending = /*loading_status*/
        ((_ = r[1]) == null ? void 0 : _.status) === "pending"), c[0] & /*likeable*/
        1024 && (u.likeable = /*likeable*/
        r[10]), c[0] & /*clickable*/
        2048 && (u.clickable = /*clickable*/
        r[11]), c[0] & /*label*/
        16 && (u.label = /*label*/
        r[4]), c[0] & /*action_label*/
        32 && (u.action_label = /*action_label*/
        r[5]), c[0] & /*value*/
        512 && (u.value = /*value*/
        r[9]), c[0] & /*root*/
        8388608 && (u.root = /*root*/
        r[23]), c[0] & /*proxy_url*/
        16777216 && (u.proxy_url = /*proxy_url*/
        r[24]), c[0] & /*show_label*/
        4 && (u.show_label = /*show_label*/
        r[2]), c[0] & /*object_fit*/
        2097152 && (u.object_fit = /*object_fit*/
        r[21]), c[0] & /*_load_more_button_props*/
        67108864 && (u.load_more_button_props = /*_load_more_button_props*/
        r[26]), c[0] & /*has_more*/
        8 && (u.has_more = /*has_more*/
        r[3]), c[0] & /*columns*/
        32768 && (u.columns = /*columns*/
        r[15]), c[0] & /*height*/
        131072 && (u.height = /*height*/
        r[17]), c[0] & /*preview*/
        262144 && (u.preview = /*preview*/
        r[18]), c[0] & /*gap*/
        65536 && (u.gap = /*gap*/
        r[16]), c[0] & /*allow_preview*/
        524288 && (u.allow_preview = /*allow_preview*/
        r[19]), c[0] & /*show_share_button*/
        1048576 && (u.show_share_button = /*show_share_button*/
        r[20]), c[0] & /*show_download_button*/
        4194304 && (u.show_download_button = /*show_download_button*/
        r[22]), c[0] & /*gradio*/
        33554432 && (u.i18n = /*gradio*/
        r[25].i18n), !n && c[0] & /*selected_index*/
        1 && (n = !0, u.selected_index = /*selected_index*/
        r[0], pd(() => n = !1)), t.$set(u);
      },
      i(r) {
        i || (Kt(o), Kt(t.$$.fragment, r), i = !0);
      },
      o(r) {
        yn(o), yn(t.$$.fragment, r), i = !1;
      },
      d(r) {
        r && Td(e), o && o.d(r), Mi(t, r);
      }
    }
  );
}
function Md(l) {
  let e, t;
  return e = new ts({
    props: {
      visible: (
        /*visible*/
        l[8]
      ),
      variant: "solid",
      padding: !1,
      elem_id: (
        /*elem_id*/
        l[6]
      ),
      elem_classes: (
        /*elem_classes*/
        l[7]
      ),
      container: (
        /*container*/
        l[12]
      ),
      scale: (
        /*scale*/
        l[13]
      ),
      min_width: (
        /*min_width*/
        l[14]
      ),
      allow_overflow: !1,
      $$slots: {
        default: [Od]
      },
      $$scope: {
        ctx: l
      }
    }
  }), {
    c() {
      Oi(e.$$.fragment);
    },
    l(n) {
      Ni(e.$$.fragment, n);
    },
    m(n, i) {
      Pi(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*visible*/
      256 && (o.visible = /*visible*/
      n[8]), i[0] & /*elem_id*/
      64 && (o.elem_id = /*elem_id*/
      n[6]), i[0] & /*elem_classes*/
      128 && (o.elem_classes = /*elem_classes*/
      n[7]), i[0] & /*container*/
      4096 && (o.container = /*container*/
      n[12]), i[0] & /*scale*/
      8192 && (o.scale = /*scale*/
      n[13]), i[0] & /*min_width*/
      16384 && (o.min_width = /*min_width*/
      n[14]), i[0] & /*loading_status, likeable, clickable, label, action_label, value, root, proxy_url, show_label, object_fit, _load_more_button_props, has_more, columns, height, preview, gap, allow_preview, show_share_button, show_download_button, gradio, selected_index*/
      134188607 | i[1] & /*$$scope*/
      128 && (o.$$scope = {
        dirty: i,
        ctx: n
      }), e.$set(o);
    },
    i(n) {
      t || (Kt(e.$$.fragment, n), t = !0);
    },
    o(n) {
      yn(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Mi(e, n);
    }
  };
}
function Pd(l, e, t) {
  let {
    loading_status: n
  } = e, {
    show_label: i
  } = e, {
    has_more: o
  } = e, {
    label: s
  } = e, {
    action_label: f
  } = e, {
    elem_id: a = ""
  } = e, {
    elem_classes: r = []
  } = e, {
    visible: c = !0
  } = e, {
    value: u = null
  } = e, {
    likeable: _
  } = e, {
    clickable: m
  } = e, {
    container: p = !0
  } = e, {
    scale: y = null
  } = e, {
    min_width: C = void 0
  } = e, {
    columns: E = [2]
  } = e, {
    gap: b = 8
  } = e, {
    height: v = "auto"
  } = e, {
    preview: g
  } = e, {
    allow_preview: S = !0
  } = e, {
    selected_index: w = null
  } = e, {
    show_share_button: L = !1
  } = e, {
    object_fit: A = "cover"
  } = e, {
    show_download_button: q = !1
  } = e, {
    root: F
  } = e, {
    proxy_url: P
  } = e, {
    gradio: j
  } = e, {
    load_more_button_props: de = {}
  } = e, x = {};
  const Ae = Nd(), ee = (h) => {
    j.dispatch("like", h);
  };
  function ke(h) {
    w = h, t(0, w);
  }
  const Se = (h) => j.dispatch("click", h.detail), re = () => j.dispatch("change", u), G = (h) => ee(h.detail), z = (h) => j.dispatch("select", h.detail), Ze = (h) => j.dispatch("share", h.detail), W = (h) => j.dispatch("error", h.detail), wt = () => {
    j.dispatch("load_more", u);
  };
  return l.$$set = (h) => {
    "loading_status" in h && t(1, n = h.loading_status), "show_label" in h && t(2, i = h.show_label), "has_more" in h && t(3, o = h.has_more), "label" in h && t(4, s = h.label), "action_label" in h && t(5, f = h.action_label), "elem_id" in h && t(6, a = h.elem_id), "elem_classes" in h && t(7, r = h.elem_classes), "visible" in h && t(8, c = h.visible), "value" in h && t(9, u = h.value), "likeable" in h && t(10, _ = h.likeable), "clickable" in h && t(11, m = h.clickable), "container" in h && t(12, p = h.container), "scale" in h && t(13, y = h.scale), "min_width" in h && t(14, C = h.min_width), "columns" in h && t(15, E = h.columns), "gap" in h && t(16, b = h.gap), "height" in h && t(17, v = h.height), "preview" in h && t(18, g = h.preview), "allow_preview" in h && t(19, S = h.allow_preview), "selected_index" in h && t(0, w = h.selected_index), "show_share_button" in h && t(20, L = h.show_share_button), "object_fit" in h && t(21, A = h.object_fit), "show_download_button" in h && t(22, q = h.show_download_button), "root" in h && t(23, F = h.root), "proxy_url" in h && t(24, P = h.proxy_url), "gradio" in h && t(25, j = h.gradio), "load_more_button_props" in h && t(28, de = h.load_more_button_props);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*_load_more_button_props, load_more_button_props*/
    335544320 && t(26, x = {
      ...x,
      ...de
    }), l.$$.dirty[0] & /*selected_index*/
    1 && Ae("prop_change", {
      selected_index: w
    });
  }, [w, n, i, o, s, f, a, r, c, u, _, m, p, y, C, E, b, v, g, S, L, A, q, F, P, j, x, ee, de, ke, Se, re, G, z, Ze, W, wt];
}
class Hd extends bd {
  constructor(e) {
    super(), Ld(this, e, Pd, Md, Rd, {
      loading_status: 1,
      show_label: 2,
      has_more: 3,
      label: 4,
      action_label: 5,
      elem_id: 6,
      elem_classes: 7,
      visible: 8,
      value: 9,
      likeable: 10,
      clickable: 11,
      container: 12,
      scale: 13,
      min_width: 14,
      columns: 15,
      gap: 16,
      height: 17,
      preview: 18,
      allow_preview: 19,
      selected_index: 0,
      show_share_button: 20,
      object_fit: 21,
      show_download_button: 22,
      root: 23,
      proxy_url: 24,
      gradio: 25,
      load_more_button_props: 28
    }, null, [-1, -1]);
  }
}
export {
  gd as BaseGallery,
  Hd as default
};
