#!/usr/bin/env python3
"""
Glyph Review Server for IDC Calyptapis
A Flask app for visually reviewing font glyphs and recording design consistency assessments.
"""

import json
import os
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory, send_file

app = Flask(__name__)

# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
SVG_DIR = PROJECT_DIR / "calyptapis" / "maj"
REVIEWS_FILE = SCRIPT_DIR / "glyph_reviews.json"
WEIGHTS = ["UltraLight", "Light", "Normal", "SemiBold", "Bold", "Black"]


def load_reviews():
    """Load existing reviews from JSON file."""
    if REVIEWS_FILE.exists():
        with open(REVIEWS_FILE, "r") as f:
            return json.load(f)
    return {"reviews": {}, "metadata": {"total_glyphs": 0, "reviewed_count": 0}}


def save_reviews(data):
    """Save reviews to JSON file."""
    # Update metadata
    data["metadata"]["reviewed_count"] = len(data["reviews"])
    with open(REVIEWS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_glyphs_by_weight():
    """Get all SVG files organized by weight."""
    glyphs = {}
    for weight in WEIGHTS:
        weight_dir = SVG_DIR / weight
        if weight_dir.exists():
            svg_files = sorted([f.name for f in weight_dir.glob("*.svg")])
            glyphs[weight] = svg_files
    return glyphs


@app.route("/")
def index():
    """Serve the main review interface."""
    return send_file(SCRIPT_DIR / "review_app.html")


@app.route("/api/glyphs")
def api_glyphs():
    """Return all glyphs organized by weight."""
    glyphs = get_glyphs_by_weight()
    return jsonify(glyphs)


@app.route("/api/reviews")
def api_get_reviews():
    """Return all saved reviews."""
    return jsonify(load_reviews())


@app.route("/api/reviews", methods=["POST"])
def api_save_review():
    """Save a review for a specific glyph."""
    data = request.json
    weight = data.get("weight")
    glyph = data.get("glyph")
    sentiment = data.get("sentiment")  # "up" or "down"
    comment = data.get("comment", "")

    if not all([weight, glyph, sentiment]):
        return jsonify({"error": "Missing required fields"}), 400

    reviews = load_reviews()
    review_key = f"{weight}/{glyph}"
    reviews["reviews"][review_key] = {
        "weight": weight,
        "glyph": glyph,
        "sentiment": sentiment,
        "comment": comment,
    }

    # Update total glyphs count if not set
    if reviews["metadata"]["total_glyphs"] == 0:
        glyphs = get_glyphs_by_weight()
        total = sum(len(files) for files in glyphs.values())
        reviews["metadata"]["total_glyphs"] = total

    save_reviews(reviews)
    return jsonify({"success": True, "reviewed_count": len(reviews["reviews"])})


@app.route("/api/reviews/<weight>/<glyph>", methods=["DELETE"])
def api_delete_review(weight, glyph):
    """Delete a review for a specific glyph."""
    reviews = load_reviews()
    review_key = f"{weight}/{glyph}"
    if review_key in reviews["reviews"]:
        del reviews["reviews"][review_key]
        save_reviews(reviews)
    return jsonify({"success": True})


@app.route("/svg/<weight>/<filename>")
def serve_svg(weight, filename):
    """Serve SVG files from the weight directories."""
    return send_from_directory(SVG_DIR / weight, filename)


if __name__ == "__main__":
    print(f"Starting Glyph Review Server...")
    print(f"SVG directory: {SVG_DIR}")
    print(f"Reviews file: {REVIEWS_FILE}")
    print(f"Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
