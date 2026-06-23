# app.py
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from graph import app

st.set_page_config(page_title="Agentic Transfer Validator", layout="wide")
st.title("⚽ Agentic Transfer Market Validator")
st.markdown("---")

rumor_input = st.text_area(
    "Enter a transfer rumor text:",
    value="Anthony Gordon to Barcelona for 80m EUR reported by Sky Sports",
    height=100,
)

if st.button("Validate Rumor", type="primary"):
    if not rumor_input.strip():
        st.error("Please enter a valid rumor claim.")
    else:
        with st.spinner("Running the rumor through the LangGraph pipeline..."):
            result = app.invoke({"rumor": {"raw_text": rumor_input}})

        cred = result.get("credibility") or {}
        fit  = result.get("fit") or {}
        val  = result.get("value") or {}
        vd   = result.get("verdict") or {}

        st.subheader("📋 Parsed Rumor Metadata")
        st.json(result.get("rumor", {}))
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔍 Credibility Analysis")
            st.metric("Source Confidence", f"{cred.get('confidence', 0)}%")
            st.write(f"**Tier:** {cred.get('tier', 'N/A')}")
            st.write(cred.get("rationale", ""))

        with col2:
            st.subheader("📊 Performance & Value")
            if fit.get("computed"):
                st.metric("Tactical Fit Score", f"{fit.get('fit_score', 0)}/100")
                st.write(f"**Target Role:** {fit.get('role')}")
                if fit.get("strengths"):
                    st.write("**Strengths:** " + ", ".join(fit["strengths"]))
                if fit.get("gaps"):
                    st.write("**Gaps:** " + ", ".join(fit["gaps"]))
            else:
                st.info("⚠️ Tactical fit not computed — player not in the cached dataset.")
            if val.get("found"):
                st.write(f"**Market Value:** €{val['market_value_eur']:,}")
                if val.get("premium_pct") is not None:
                    st.write(f"**Premium vs reported fee:** {val['premium_pct']}%")

        st.markdown("---")
        st.subheader("🎯 Executive Verdict")
        rec = vd.get("recommendation", "Caution")
        color = {"Proceed": "green", "Caution": "orange"}.get(rec, "red")
        st.markdown(f"### :{color}[**{rec}**] ({vd.get('confidence', 0)}% confidence)")
        st.write(vd.get("reasoning", ""))
        if vd.get("key_factors"):
            st.write("**Key Decision Factors:**")
            for factor in vd["key_factors"]:
                st.write(f"- {factor}")

        if result.get("errors"):
            st.caption("Data caveats: " + "; ".join(result["errors"]))