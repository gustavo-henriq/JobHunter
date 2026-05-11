import json
from pathlib import Path


PROFILE_PATH = Path(__file__).resolve().parent / "profiles.json"


def load_profiles():
    with PROFILE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_profile(profile_id):
    profiles = load_profiles()
    for profile in profiles:
        if profile.get("profile_id") == profile_id:
            return profile
    return None


def build_profile_prompt(profile_id):
    profile = get_profile(profile_id)
    if profile is None:
        return None

    languages = profile.get("languages", {})
    language_text = ", ".join(
        f"{language}: {level}" for language, level in languages.items()
    ) or "not specified"

    skills = ", ".join(profile.get("skills", [])) or "not specified"
    target_roles = ", ".join(profile.get("target_roles", [])) or "not specified"
    target_areas = ", ".join(profile.get("target_areas", [])) or "not specified"
    avoid_keywords = ", ".join(profile.get("avoid_keywords", [])) or "none"
    preferred_keywords = ", ".join(profile.get("preferred_keywords", [])) or "none"
    career_stage = profile.get("career_stage") or "not specified"
    work_mode = profile.get("work_mode") or "not specified"
    salary_expectation = profile.get("salary_expectation") or "not specified"
    location = profile.get("location") or "not specified"

    return (
        f"This is the profile '{profile_id}'. "
        f"The candidate career stage is {career_stage}. "
        f"The main target roles are {target_roles}. "
        f"The target professional areas are {target_areas}. "
        f"The main skills are {skills}. "
        f"Preferred keywords are {preferred_keywords}. "
        f"Avoid these keywords: {avoid_keywords}. "
        f"Preferred work mode: {work_mode}. "
        f"Salary expectation: {salary_expectation}. "
        f"Location: {location}. "
        f"Languages: {language_text}."
    )
