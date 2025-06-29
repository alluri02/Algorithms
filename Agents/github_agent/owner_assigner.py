"""
Owner assignment logic using rules and AI analysis.
"""

import time
import yaml
from typing import List, Dict, Any, Optional
from pathlib import Path

from .config import Settings
from .models import IssueData, SummaryResult, AssignmentResult, AssignmentRule


class OwnerAssigner:
    """Handles intelligent owner assignment for issues."""
    
    def __init__(self, settings: Settings):
        """Initialize the owner assigner."""
        self.settings = settings
        self.assignment_rules: List[AssignmentRule] = []
        self._load_assignment_rules()
    
    async def assign_owner(
        self, 
        issue_data: IssueData, 
        summary_result: SummaryResult
    ) -> AssignmentResult:
        """
        Assign appropriate owner to an issue.
        
        Args:
            issue_data: Issue data
            summary_result: AI-generated summary
            
        Returns:
            AssignmentResult with assignment decision
        """
        start_time = time.time()
        
        # Analyze issue and find matching rules
        matched_rules = self._find_matching_rules(issue_data, summary_result)
        
        # Calculate assignment based on rules
        assignment = self._calculate_assignment(matched_rules, issue_data)
        
        processing_time = time.time() - start_time
        
        return AssignmentResult(
            issue_number=issue_data.number,
            assigned_owner=assignment.get("owner"),
            confidence_score=assignment.get("confidence", 0.0),
            reasoning=assignment.get("reasoning", "No matching rules found"),
            matched_rules=[rule.name for rule in matched_rules],
            alternative_owners=assignment.get("alternatives", []),
            processing_time=processing_time
        )
    
    async def health_check(self) -> bool:
        """Check assignment rules and configuration."""
        try:
            return len(self.assignment_rules) > 0
        except Exception:
            return False
    
    def _load_assignment_rules(self):
        """Load assignment rules from configuration file."""
        try:
            rules_file = Path(self.settings.assignment_rules_file)
            if not rules_file.exists():
                print(f"Assignment rules file not found: {rules_file}")
                self._create_default_rules()
                return
            
            with open(rules_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            rules_data = config.get('assignment_rules', [])
            self.assignment_rules = [
                AssignmentRule(**rule_data) for rule_data in rules_data
            ]
            
            print(f"Loaded {len(self.assignment_rules)} assignment rules")
            
        except Exception as e:
            print(f"Error loading assignment rules: {e}")
            self._create_default_rules()
    
    def _create_default_rules(self):
        """Create default assignment rules."""
        self.assignment_rules = [
            AssignmentRule(
                name="Bug Reports",
                keywords=["bug", "error", "crash", "broken", "issue"],
                labels=["bug"],
                owners=["developer1", "maintainer"],
                priority=2
            ),
            AssignmentRule(
                name="Feature Requests",
                keywords=["feature", "enhancement", "improvement", "add"],
                labels=["enhancement", "feature"],
                owners=["product_manager", "lead_developer"],
                priority=2
            ),
            AssignmentRule(
                name="Documentation",
                keywords=["documentation", "docs", "readme", "guide"],
                labels=["documentation"],
                owners=["tech_writer", "maintainer"],
                priority=1
            )
        ]
    
    def _find_matching_rules(
        self, 
        issue_data: IssueData, 
        summary_result: SummaryResult
    ) -> List[AssignmentRule]:
        """Find rules that match the issue."""
        matched_rules = []
        
        # Combine text for analysis
        issue_text = f"{issue_data.title} {issue_data.body}".lower()
        summary_text = summary_result.summary.lower()
        combined_text = f"{issue_text} {summary_text}"
        
        for rule in self.assignment_rules:
            match_score = 0
            
            # Check keyword matches
            keyword_matches = sum(
                1 for keyword in rule.keywords 
                if keyword.lower() in combined_text
            )
            if keyword_matches > 0:
                match_score += keyword_matches * 2
            
            # Check label matches
            label_matches = sum(
                1 for label in rule.labels 
                if label in issue_data.labels
            )
            if label_matches > 0:
                match_score += label_matches * 3
            
            # Apply rule priority
            match_score = match_score * rule.priority
            
            if match_score > 0:
                rule.match_score = match_score
                matched_rules.append(rule)
        
        # Sort by match score (descending)
        matched_rules.sort(key=lambda r: getattr(r, 'match_score', 0), reverse=True)
        
        return matched_rules
    
    def _calculate_assignment(
        self, 
        matched_rules: List[AssignmentRule], 
        issue_data: IssueData
    ) -> Dict[str, Any]:
        """Calculate the best assignment based on matched rules."""
        if not matched_rules:
            return {
                "owner": None,
                "confidence": 0.0,
                "reasoning": "No matching assignment rules found",
                "alternatives": []
            }
        
        # Use the highest scoring rule
        best_rule = matched_rules[0]
        best_owner = best_rule.owners[0] if best_rule.owners else None
        
        # Calculate confidence based on match quality
        max_possible_score = len(best_rule.keywords) * 2 + len(best_rule.labels) * 3
        max_possible_score = max_possible_score * best_rule.priority
        
        actual_score = getattr(best_rule, 'match_score', 0)
        confidence = min(actual_score / max(max_possible_score, 1), 1.0)
        
        # Collect alternative owners
        alternatives = []
        for rule in matched_rules[:3]:  # Top 3 rules
            alternatives.extend(rule.owners)
        
        # Remove duplicates and the selected owner
        alternatives = list(set(alternatives))
        if best_owner in alternatives:
            alternatives.remove(best_owner)
        
        reasoning = f"Matched rule '{best_rule.name}' with confidence {confidence:.2f}"
        if len(matched_rules) > 1:
            reasoning += f" (from {len(matched_rules)} matching rules)"
        
        return {
            "owner": best_owner,
            "confidence": confidence,
            "reasoning": reasoning,
            "alternatives": alternatives[:3]  # Limit to top 3
        }
