import pytest
from playwright.sync_api import expect
import string
import random

class TestLeadNegative:
    
    @pytest.fixture
    def lead_form(self, browser_page):
        """Open new lead form for each negative test"""
        browser_page.open_new_lead()
        return browser_page
    
    # ========== NAME FIELD NEGATIVE TESTS ==========
    
    @pytest.mark.parametrize("name,expected_warning", [
        ("", "Name is required"),
        ("   ", "Name is required"),
        ("John@Doe", "Invalid name"),
        ("Jane#Smith", "Invalid name"),
        ("Test$User", "Invalid name"),
        ("Name%With%Special", "Invalid name"),
        ("User&Name", "Invalid name"),
        ("Test*Name", "Invalid name"),
        ("123456789", "Invalid name"),
        ("   John   ", "Invalid name"),
    ])
    def test_invalid_name_formats(self, browser_page, lead_form, name, expected_warning):
        """Test invalid name formats - should show warning"""
        browser_page.page.get_by_placeholder("e.g. Jane Smith").fill(name)
        browser_page.page.get_by_placeholder("Enter Phone Number").fill("1234567890")
        browser_page.page.locator('#email').fill("test@test.com")
        
        browser_page.submit_lead()
        browser_page.wait('short')
        
        warning_visible = browser_page.page.get_by_text(expected_warning).is_visible()
        
        if not warning_visible:
            alternative_warnings = ["Invalid name", "Name is required", "Invalid input", "Please enter a valid name"]
            for alt_warning in alternative_warnings:
                if browser_page.page.get_by_text(alt_warning).is_visible():
                    warning_visible = True
                    break
        
        assert warning_visible, f"Name '{name}' should show warning: {expected_warning}"
        browser_page.open_new_lead()
    
    @pytest.mark.parametrize("name,expected_warning", [
        ("a" * 256, "Name is too long"),
        ("a" * 500, "Name is too long"),
        ("a" * 1000, "Name is too long"),
    ])
    def test_very_long_name(self, browser_page, lead_form, name, expected_warning):
        """Test very long name - should show warning"""
        browser_page.page.get_by_placeholder("e.g. Jane Smith").fill(name)
        browser_page.page.get_by_placeholder("Enter Phone Number").fill("1234567890")
        browser_page.page.locator('#email').fill("test@test.com")
        
        browser_page.submit_lead()
        browser_page.wait('short')
        
        warning_visible = browser_page.page.get_by_text(expected_warning).is_visible()
        
        if not warning_visible:
            alternative_warnings = ["Name is too long", "Maximum length exceeded", "Invalid input"]
            for alt_warning in alternative_warnings:
                if browser_page.page.get_by_text(alt_warning).is_visible():
                    warning_visible = True
                    break
        
        assert warning_visible, f"Name length {len(name)} should show warning: {expected_warning}"
        browser_page.open_new_lead()
    
    # ========== PHONE FIELD NEGATIVE TESTS ==========
    
    @pytest.mark.parametrize("phone,expected_warning", [
        ("", "Phone is required"),
        ("ABC", "Invalid phone number"),
        ("ABCDEFGHIJ", "Invalid phone number"),
        ("123", "Phone number must be at least"),
        ("12", "Phone number must be at least"),
        ("12345678901234567890", "Phone number is too long"),
        ("123-456-7890", "Invalid phone number"),
        ("(123) 456-7890", "Invalid phone number"),
        ("+1-234-567-8900", "Invalid phone number"),
        ("abc123def", "Invalid phone number"),
    ])
    def test_invalid_phone_formats(self, browser_page, lead_form, phone, expected_warning):
        """Test invalid phone formats - should show warning"""
        browser_page.page.get_by_placeholder("e.g. Jane Smith").fill("Test Lead")
        browser_page.page.get_by_placeholder("Enter Phone Number").clear()
        browser_page.page.get_by_placeholder("Enter Phone Number").fill(phone)
        browser_page.page.locator('#email').fill("test@test.com")
        
        browser_page.submit_lead()
        browser_page.wait('short')
        
        warning_visible = browser_page.page.get_by_text(expected_warning).is_visible()
        
        if not warning_visible:
            alternative_warnings = ["Invalid phone", "Phone is required", "Invalid input", "Please enter a valid phone"]
            for alt_warning in alternative_warnings:
                if browser_page.page.get_by_text(alt_warning).is_visible():
                    warning_visible = True
                    break
        
        assert warning_visible, f"Phone '{phone}' should show warning: {expected_warning}"
        browser_page.open_new_lead()
    
    # ========== EMAIL FIELD NEGATIVE TESTS ==========
    
    @pytest.mark.parametrize("email,expected_warning", [
        ("", "Email is required"),
        ("test", "Invalid email"),
        ("test@", "Invalid email"),
        ("@test.com", "Invalid email"),
        ("test@test", "Invalid email"),
        ("test@.com", "Invalid email"),
        ("test test@test.com", "Invalid email"),
        ("test@test..com", "Invalid email"),
        ("test@test.c", "Invalid email"),
        ("test@@test.com", "Invalid email"),
        ("test@test@test.com", "Invalid email"),
        (".test@test.com", "Invalid email"),
        ("test.@test.com", "Invalid email"),
    ])
    def test_invalid_email_formats(self, browser_page, lead_form, email, expected_warning):
        """Test invalid email formats - should show warning"""
        browser_page.page.get_by_placeholder("e.g. Jane Smith").fill("Test Lead")
        browser_page.page.get_by_placeholder("Enter Phone Number").fill("1234567890")
        browser_page.page.locator('#email').clear()
        browser_page.page.locator('#email').fill(email)
        
        browser_page.submit_lead()
        browser_page.wait('short')
        
        warning_visible = browser_page.page.get_by_text(expected_warning).is_visible()
        
        if not warning_visible:
            alternative_warnings = ["Invalid email", "Email is required", "Invalid input", "Please enter a valid email"]
            for alt_warning in alternative_warnings:
                if browser_page.page.get_by_text(alt_warning).is_visible():
                    warning_visible = True
                    break
        
        assert warning_visible, f"Email '{email}' should show warning: {expected_warning}"
        browser_page.open_new_lead()
    
    # ========== BUDGET FIELD NEGATIVE TESTS ==========
    
    @pytest.mark.parametrize("budget,expected_warning", [
        ("", "Budget must be a number"),
        ("abc", "Budget must be a number"),
        ("-1000", "Budget must be positive"),
        ("0", "Budget must be greater than 0"),
        ("-1", "Budget must be positive"),
        ("12.34", "Budget must be a whole number"),
        ("99999999999999999999", "Budget is too large"),
        ("10,000", "Budget must be a number"),
        ("$1000", "Budget must be a number"),
    ])
    def test_invalid_budget_formats(self, browser_page, lead_form, budget, expected_warning):
        """Test invalid budget formats - should show warning"""
        browser_page.page.get_by_placeholder("e.g. Jane Smith").fill("Test Lead")
        browser_page.page.get_by_placeholder("Enter Phone Number").fill("1234567890")
        browser_page.page.locator('#email').fill("test@test.com")
        browser_page.page.locator('#budget').clear()
        browser_page.page.locator('#budget').fill(budget)
        
        browser_page.submit_lead()
        browser_page.wait('short')
        
        warning_visible = browser_page.page.get_by_text(expected_warning).is_visible()
        
        if not warning_visible:
            alternative_warnings = ["Invalid budget", "Budget is required", "Invalid input", "Please enter a valid budget"]
            for alt_warning in alternative_warnings:
                if browser_page.page.get_by_text(alt_warning).is_visible():
                    warning_visible = True
                    break
        
        assert warning_visible, f"Budget '{budget}' should show warning: {expected_warning}"
        browser_page.open_new_lead()
    
    # ========== REFERRED BY NEGATIVE TESTS ==========
    
    @pytest.mark.parametrize("referred_by,expected_warning", [
        ("", "Invalid referred by"),
        ("   ", "Invalid referred by"),
        ("John@Doe#123", "Invalid characters detected"),
        ("<script>alert('xss')</script>", "Invalid characters detected"),
        ("'; DROP TABLE users; --", "Invalid characters detected"),
        ("test" * 100, "Invalid referred by"),
        ("test@test.com", "Invalid referred by"),
        ("1234567890", "Invalid referred by"),
    ])
    def test_invalid_referred_by(self, browser_page, lead_form, referred_by, expected_warning):
        """Test invalid referred by formats - should show warning"""
        browser_page.page.get_by_placeholder("e.g. Jane Smith").fill("Test Lead")
        browser_page.page.get_by_placeholder("Enter Phone Number").fill("1234567890")
        browser_page.page.locator('#email').fill("test@test.com")
        browser_page.page.get_by_placeholder("Referred By").clear()
        browser_page.page.get_by_placeholder("Referred By").fill(referred_by)
        
        browser_page.submit_lead()
        browser_page.wait('short')
        
        warning_visible = browser_page.page.get_by_text(expected_warning).is_visible()
        
        if not warning_visible:
            alternative_warnings = ["Invalid input", "Invalid characters", "Invalid referred by"]
            for alt_warning in alternative_warnings:
                if browser_page.page.get_by_text(alt_warning).is_visible():
                    warning_visible = True
                    break
        
        assert warning_visible, f"Referred by '{referred_by}' should show warning: {expected_warning}"
        browser_page.open_new_lead()
    
    # ========== LOCATION FIELD NEGATIVE TESTS ==========
    
    @pytest.mark.parametrize("location,expected_warning", [
        ("", "Location is required"),
        ("   ", "Location is required"),
        ("a" * 500, "Location is too long"),
        ("a" * 1000, "Location is too long"),
        ("<script>alert('xss')</script>", "Invalid characters detected"),
        ("'; DROP TABLE users; --", "Invalid characters detected"),
    ])
    def test_invalid_location_formats(self, browser_page, lead_form, location, expected_warning):
        """Test invalid location formats - should show warning"""
        browser_page.page.get_by_placeholder("e.g. Jane Smith").fill("Test Lead")
        browser_page.page.get_by_placeholder("Enter Phone Number").fill("1234567890")
        browser_page.page.locator('#email').fill("test@test.com")
        browser_page.page.locator('#address').clear()
        browser_page.page.locator('#address').fill(location)
        
        browser_page.submit_lead()
        browser_page.wait('short')
        
        warning_visible = browser_page.page.get_by_text(expected_warning).is_visible()
        
        if not warning_visible:
            alternative_warnings = ["Invalid location", "Location is required", "Invalid input", "Invalid characters"]
            for alt_warning in alternative_warnings:
                if browser_page.page.get_by_text(alt_warning).is_visible():
                    warning_visible = True
                    break
        
        assert warning_visible, f"Location '{location}' should show warning: {expected_warning}"
        browser_page.open_new_lead()
    
    # ========== INTEREST AREA NEGATIVE TESTS ==========
    
    @pytest.mark.parametrize("interest,expected_warning", [
        ("", "Interest area is required"),
        ("   ", "Interest area is required"),
        ("a" * 500, "Interest area is too long"),
        ("<script>alert('xss')</script>", "Invalid characters detected"),
        ("'; DROP TABLE users; --", "Invalid characters detected"),
    ])
    def test_invalid_interest_area(self, browser_page, lead_form, interest, expected_warning):
        """Test invalid interest area formats - should show warning"""
        browser_page.page.get_by_placeholder("e.g. Jane Smith").fill("Test Lead")
        browser_page.page.get_by_placeholder("Enter Phone Number").fill("1234567890")
        browser_page.page.locator('#email').fill("test@test.com")
        browser_page.page.locator('#interest_area').clear()
        browser_page.page.locator('#interest_area').fill(interest)
        
        browser_page.submit_lead()
        browser_page.wait('short')
        
        warning_visible = browser_page.page.get_by_text(expected_warning).is_visible()
        
        if not warning_visible:
            alternative_warnings = ["Invalid interest", "Interest area is required", "Invalid input", "Invalid characters"]
            for alt_warning in alternative_warnings:
                if browser_page.page.get_by_text(alt_warning).is_visible():
                    warning_visible = True
                    break
        
        assert warning_visible, f"Interest '{interest}' should show warning: {expected_warning}"
        browser_page.open_new_lead()
    
    # ========== NOTES FIELD NEGATIVE TESTS ==========
    
    @pytest.mark.parametrize("notes,expected_warning", [
        ("a" * 2000, "Notes is too long"),
        ("<script>alert('xss')</script>", "Invalid characters detected"),
        ("'; DROP TABLE users; --", "Invalid characters detected"),
    ])
    def test_invalid_notes(self, browser_page, lead_form, notes, expected_warning):
        """Test invalid notes formats - should show warning"""
        browser_page.page.get_by_placeholder("e.g. Jane Smith").fill("Test Lead")
        browser_page.page.get_by_placeholder("Enter Phone Number").fill("1234567890")
        browser_page.page.locator('#email').fill("test@test.com")
        browser_page.page.get_by_placeholder("Add any specific requirement here...").clear()
        browser_page.page.get_by_placeholder("Add any specific requirement here...").fill(notes)
        
        browser_page.submit_lead()
        browser_page.wait('short')
        
        warning_visible = browser_page.page.get_by_text(expected_warning).is_visible()
        
        if not warning_visible:
            alternative_warnings = ["Invalid notes", "Notes is too long", "Invalid input", "Invalid characters"]
            for alt_warning in alternative_warnings:
                if browser_page.page.get_by_text(alt_warning).is_visible():
                    warning_visible = True
                    break
        
        assert warning_visible, f"Notes '{notes[:50]}...' should show warning: {expected_warning}"
        browser_page.open_new_lead()
    
    # ========== SECURITY TESTS ==========
    
    @pytest.mark.parametrize("payload,payload_type,expected_warning", [
        ("'; DROP TABLE leads; --", "SQL Injection", "Invalid characters detected"),
        ("'; DELETE FROM leads; --", "SQL Injection", "Invalid characters detected"),
        ("'; UPDATE leads SET name='hacked'; --", "SQL Injection", "Invalid characters detected"),
        ("<script>alert('XSS')</script>", "XSS", "Invalid characters detected"),
        ("<img src=x onerror=alert('XSS')>", "XSS", "Invalid characters detected"),
        ("<iframe src='javascript:alert(\"XSS\")'>", "XSS", "Invalid characters detected"),
        ("<body onload=alert('XSS')>", "XSS", "Invalid characters detected"),
        ("${7*7}", "Template Injection", "Invalid characters detected"),
        ("{{7*7}}", "Template Injection", "Invalid characters detected"),
        ("../../etc/passwd", "Path Traversal", "Invalid characters detected"),
        ("%00", "Null Byte Injection", "Invalid characters detected"),
    ])
    def test_security_payloads(self, browser_page, lead_form, payload, payload_type, expected_warning):
        """Test security payloads - should show warning and NOT be accepted"""
        # Test in name field
        browser_page.page.get_by_placeholder("e.g. Jane Smith").fill(payload)
        browser_page.page.get_by_placeholder("Enter Phone Number").fill("1234567890")
        browser_page.page.locator('#email').fill("test@test.com")
        
        browser_page.submit_lead()
        browser_page.wait('short')
        
        warning_visible = browser_page.page.get_by_text(expected_warning).is_visible()
        
        if not warning_visible:
            alternative_warnings = ["Invalid input", "Invalid characters", "Invalid name"]
            for alt_warning in alternative_warnings:
                if browser_page.page.get_by_text(alt_warning).is_visible():
                    warning_visible = True
                    break
        
        assert warning_visible, f"Security risk: {payload_type} payload '{payload}' should show warning: {expected_warning}"
        browser_page.open_new_lead()
    
    # ========== COMBINED NEGATIVE TESTS ==========
    
    @pytest.mark.parametrize("test_case", [
        ("all_empty", "All fields should show required warnings"),
        ("all_spaces", "All fields with spaces should show required warnings"),
    ])
    def test_combined_negative_scenarios(self, browser_page, lead_form, test_case):
        """Test combined negative scenarios"""
        test_name, expected = test_case
        
        if test_name == "all_empty":
            # Submit with all fields empty
            browser_page.submit_lead()
            browser_page.wait('short')
            
            required_warnings = ["Name is required", "Phone is required", "Email is required"]
            visible_warnings = []
            
            for warning in required_warnings:
                if browser_page.page.get_by_text(warning).is_visible():
                    visible_warnings.append(warning)
            
            missing_warnings = [w for w in required_warnings if w not in visible_warnings]
            assert len(missing_warnings) == 0, f"Missing warnings for empty fields: {missing_warnings}"
            
        elif test_name == "all_spaces":
            # Fill all fields with spaces
            browser_page.page.get_by_placeholder("e.g. Jane Smith").fill("   ")
            browser_page.page.get_by_placeholder("Enter Phone Number").fill("   ")
            browser_page.page.locator('#email').fill("   ")
            browser_page.page.locator('#address').fill("   ")
            browser_page.page.get_by_placeholder("Referred By").fill("   ")
            browser_page.page.locator('#budget').fill("   ")
            browser_page.page.locator('#interest_area').fill("   ")
            browser_page.page.get_by_placeholder("Add any specific requirement here...").fill("   ")
            
            browser_page.submit_lead()
            browser_page.wait('short')
            
            required_warnings = ["Name is required", "Phone is required", "Email is required"]
            visible_warnings = []
            
            for warning in required_warnings:
                if browser_page.page.get_by_text(warning).is_visible():
                    visible_warnings.append(warning)
            
            missing_warnings = [w for w in required_warnings if w not in visible_warnings]
            assert len(missing_warnings) == 0, f"Missing warnings for fields with spaces: {missing_warnings}"