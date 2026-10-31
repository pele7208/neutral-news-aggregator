from __future__ import annotations

import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    short_name: Mapped[str] = mapped_column(String(64))
    url: Mapped[str] = mapped_column(String(512))
    lean: Mapped[str] = mapped_column(String(32))
    factual_rating: Mapped[str] = mapped_column(String(32))
    is_wire_service: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    articles: Mapped[list["Article"]] = relationship(back_populates="source")


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(2048), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(1024))
    snippet: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    published_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    fetched_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.id"))
    is_opinion: Mapped[bool] = mapped_column(Boolean, default=False)
    lean: Mapped[str] = mapped_column(String(32), default="center")

    source: Mapped["Source"] = relationship(back_populates="articles")
    story_links: Mapped[list["StoryArticle"]] = relationship(back_populates="article")


class Story(Base):
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    headline: Mapped[str] = mapped_column(String(1024))
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    disputed_claims: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timeline_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    significance_score: Mapped[float] = mapped_column(Float, default=0.0)
    lean_distribution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    coverage_analysis: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    loaded_terms_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    topic: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    first_seen_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    story_links: Mapped[list["StoryArticle"]] = relationship(
        back_populates="story", cascade="all, delete-orphan"
    )
    corrections: Mapped[list["Correction"]] = relationship(back_populates="story")


class StoryArticle(Base):
    __tablename__ = "story_articles"

    story_id: Mapped[int] = mapped_column(ForeignKey("stories.id"), primary_key=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"), primary_key=True)

    story: Mapped["Story"] = relationship(back_populates="story_links")
    article: Mapped["Article"] = relationship(back_populates="story_links")


class Correction(Base):
    __tablename__ = "corrections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    story_id: Mapped[Optional[int]] = mapped_column(ForeignKey("stories.id"), nullable=True)
    description: Mapped[str] = mapped_column(Text)
    corrected_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    story: Mapped[Optional["Story"]] = relationship(back_populates="corrections")


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    started_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    finished_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    articles_fetched: Mapped[int] = mapped_column(Integer, default=0)
    stories_created: Mapped[int] = mapped_column(Integer, default=0)
    stories_updated: Mapped[int] = mapped_column(Integer, default=0)
    errors: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="running")
